# Copyright (c) 2019, 2020 Martin Lafaix (martin.lafaix@external.engie.com)
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0

"""
**zabel** clusters.

This module depends on the public **pyjwt** and **pyyaml** libraries.

https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md

etcd and clusters:

<https://medium.com/better-programming/a-closer-look-at-etcd-the-brain-of-a-kubernetes-cluster-788c8ea759a5>

etcd keys follows the kubernetes conventions:

/registry/{resource}/{namespace}/{name}

TODO

API Servers

https://kubernetes.io/docs/tasks/access-kubernetes-api/setup-extension-api-server/
https://github.com/kubernetes/sample-apiserver
https://github.com/kubernetes-sigs/apiserver-builder-alpha
https://github.com/kubernetes-sigs/kubebuilder

system:controller:service-controller

https://stackoverflow.com/questions/44374215/how-do-i-specify-url-resolution-in-pythons-requests-library-in-a-similar-fashio
"""

from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple, Union

import base64
import datetime
import hashlib
import json
import os
import pkgutil
import re
import uuid
import sys
import threading

import jwt
import yaml

from bottle import default_app, request, response

from zabel.commons.interfaces import ApiService
from zabel.commons.servers import (
    DEFAULT_HEADERS,
    entrypoint,
    make_status as status,
    make_items,
)
from zabel.commons.utils import patch as patchdict

from .environ import EnvironLocal
from .openapi import get_openapi
from .etcd3 import client, Event, PutEvent
from .resolver import (
    add as add_resolver,
    get as get_resolver,
    remove as remove_resolver,
)


########################################################################
## Settings

SA_KEY_FILES = ['/etc/zabel/zabel-publickey']


########################################################################
## Constants

Object = Dict[str, Any]

NAME_PATTERN = r'^[0-9a-zA-Z]+([0-9A-Za-z-_.]*[0-9a-zA-Z])?$'
LABEL_PATTERN = r'^([^/]+/)?([0-9A-Za-z-_.]{1,63})$'
DNS_LABEL_PATTERN = r'^(?![0-9]+$)(?!-)[a-z0-9-]{1,63}(?<!-)$'

KEY = r'[a-z0-9A-Z-_./]+'
VALUE = r'[a-z0-9A-Z-_.]+'
EQUAL_EXPR = rf'^({KEY})\s*([=!]?=)\s*({VALUE})(?:,|$)'
SET_EXPR = rf'^({KEY})\s+(in|notin)\s+\(({VALUE}(\s*,\s*{VALUE})*)\)(?:,|$)'
EXISTS_EXPR = rf'^{KEY}(?:,|$)'
NEXISTS_EXPR = rf'^!{KEY}(?:,|$)'


########################################################################
## Routes

API_ROUTE = '/api'
APIGROUP_ROUTE = '/apis'

APISERVICE_ROUTES = [
    f'{API_ROUTE}/v1',
    f'{APIGROUP_ROUTE}/{{group}}/{{version}}',
]
CLUSTER_ROUTES = [f'{root}/{{kind}}' for root in APISERVICE_ROUTES]
NAMESPACED_ROUTES = [
    f'{root}/namespaces/{{namespace}}/{{kind}}' for root in APISERVICE_ROUTES
]
CREATE_ROUTES = CLUSTER_ROUTES + NAMESPACED_ROUTES
DIRECT_ROUTES = [f'{root}/{{name}}' for root in CREATE_ROUTES]
STATUS_ROUTES = [f'{root}/status' for root in DIRECT_ROUTES]


########################################################################
## Keys templates

APISERVICE_PREFIX = b'/registry/apiregistration.k8s.io/apiservices/'
INGRESS_PREFIX = b'/registry/ingresses/'
DEPLOY_PREFIX = b'/registry/deployments/'
POD_PREFIX = b'/registry/pods/'
SVC_PREFIX = b'/registry/services/'
CRD_PREFIX = b'/registry/customresourcedefinitions/'

DEFAULT_NAMESPACE_KEY = b'/registry/namespaces/default'
NAMESPACED_KEY_TEMPLATE = '/registry/{resource}/{namespace}/{name}'
NAMESPACED_PREFIX_TEMPLATE = '/registry/{resource}/{namespace}/'
CLUSTER_KEY_TEMPLATE = '/registry/{resource}/{name}'
CLUSTER_PREFIX_TEMPLATE = '/registry/{resource}/'


########################################################################
## Bootstrap

APISERVICE_KEY_TEMPLATE = (
    '/registry/apiregistration.k8s.io/apiservices/{version}.{group}'
)

APISERVICE_TEMPLATE = '''{{
    "kind": "APIResourceList",
    "apiVersion": "v1",
    "groupVersion": "{group}/{version}",
    "resources": []
}}'''

DEFAULT_NAMESPACE_NAME = 'default'
DEFAULT_NAMESPACE = {
    'apiVersion': 'v1',
    'kind': 'Namespace',
    'metadata': {'name': DEFAULT_NAMESPACE_NAME},
}


########################################################################
## Helpers

## Validity checking


def _generate_hash(value: Any) -> str:
    manifest = hashlib.sha256()
    manifest.update(bytes(json.dumps(value), 'utf-8'))
    return manifest.hexdigest()[:10]


def _is_dns_label(value: Any) -> bool:
    return (
        isinstance(value, str)
        and re.match(DNS_LABEL_PATTERN, value) is not None
    )


def _is_dns_domain(value: Any) -> bool:
    if not isinstance(value, str) or len(value) > 253:
        return False
    return all(_is_dns_label(segment) for segment in value.split('.'))


def _is_label_key(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    match = re.match(LABEL_PATTERN, value)
    if not match:
        return False
    prefix, name = match.groups()
    if prefix and not _is_dns_domain(prefix[:-1]):
        return False
    return re.match(NAME_PATTERN, name) is not None


def _is_label_value(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return len(value) <= 63 and re.match(NAME_PATTERN, value) is not None


## Selectors helpers


def _split_exprs(exprs: str) -> List[str]:
    """Split a comma-separated list of expressions.

    # Required parameters

    - exprs: a string

    # Returned value

    A (possibly empty) list of _expressions_.  An expression is a
    string, stripped.
    """
    result = []
    while exprs:
        match = re.match(SET_EXPR, exprs)
        if not match:
            match = re.match(EQUAL_EXPR, exprs)
        if not match:
            match = re.match(EXISTS_EXPR, exprs)
        if not match:
            match = re.match(NEXISTS_EXPR, exprs)
        if not match:
            raise ValueError(f'Invalid expression {exprs}')
        result.append(exprs[: match.end()].strip())
        exprs = exprs[match.end() :].strip()

    return result


def _resolve_path(path: str, obj: Object) -> Tuple[bool, Optional[str]]:
    def inner(items, obj) -> Tuple[bool, Optional[str]]:
        head, rest = items[0], items[1:]
        if head in obj:
            return (True, obj[head]) if not rest else inner(rest, obj[head])
        return False, None

    return inner(path.split('.'), obj)


def _evaluate_fields(req: str, obj: Object) -> bool:
    if req == '':
        return True
    if re.match(EXISTS_EXPR, req):
        return _resolve_path(req, obj)[0]
    if re.match(NEXISTS_EXPR, req):
        return not _resolve_path(req[1:], obj)[0]
    expr = re.match(SET_EXPR, req)
    if expr:
        key, ope, list_, _ = expr.groups()
        found, value = _resolve_path(key, obj)
        if found:
            values = [v.strip() for v in list_.split(',')]
            if ope == 'in':
                return value in values
            return value not in values
        return ope == 'notin'
    expr = re.match(EQUAL_EXPR, req)
    if expr is None:
        raise ValueError(f'Invalid expression {req}.')
    key, ope, expected = expr.groups()
    found, value = _resolve_path(key, obj)
    if found:
        if ope in ('=', '=='):
            return value == expected
        return value != expected
    return ope == '!='


def _evaluate(req: str, labels: Mapping[str, str]) -> bool:
    """Evaluate whether req matches labels.

    # Required parameters

    - req: a string
    - labels: a dictionary

    # Returned value

    A boolean.  True if `req` is satisfied by `labels`, False otherwise.

    # Raised exceptions

    A _ValueError_ exception is raised if `req` is not a valid
    expression.
    """
    if req == '':
        return True
    if re.match(EXISTS_EXPR, req):
        return req in labels
    if re.match(NEXISTS_EXPR, req):
        return req[1:] not in labels
    expr = re.match(SET_EXPR, req)
    if expr:
        key, ope, list_, _ = expr.groups()
        if key in labels:
            values = [v.strip() for v in list_.split(',')]
            if ope == 'in':
                return labels[key] in values
            return labels[key] not in values
        return ope == 'notin'
    expr = re.match(EQUAL_EXPR, req)
    if expr is None:
        raise ValueError(f'Invalid expression {req}.')
    key, ope, value = expr.groups()
    if key in labels:
        if ope in ('=', '=='):
            return labels[key] == value
        return labels[key] != value
    return ope == '!='


def _match_field_selector(obj: Object, selector: str) -> bool:
    """Return True if the object matches the selector."""
    return all(_evaluate_fields(sel, obj) for sel in _split_exprs(selector))


def _match_label_selector(obj: Object, selector: str) -> bool:
    """Return True if the service matches the selector.

    An empty selector always matches.

    The complete selector feature has been implemented.  `selector` is
    of form:

        expr[,expr]*

    where `expr` is one of `key`, `!key`, or `key op value`, with
    `op` being one of `=`, `==`, or `!=`.  The
    `key in (value[, value...])` and `key notin (value[, value...])`
    set-based requirements are also implemented.

    # Required parameters

    - obj: a Definition (a dictionary)
    - selector: a string

    # Returned value

    A boolean.
    """
    return all(_evaluate(sel, obj) for sel in _split_exprs(selector))


def _read_key_files(files: Iterable[str]) -> List[str]:
    keys = []
    for keyfile in files:
        with open(keyfile) as key:
            keys.append(key.read())
    return keys


class Cluster(ApiService):
    """Clusters.

    Clusters are collections of _objects_.

    Each object has a name, a definition and a status.  Most object are
    attached to a _namespace_.

    Namespaces are objects too, but they are attached to a cluster, not
    to another namespace.  In all other aspects, they are objects.

    All objects are stored in an etcd database as JSON strings.
    """

    def __init__(
        self,
        host: str = 'localhost',
        port: int = 8080,
        service_account_key_file: Iterable[str] = SA_KEY_FILES,
    ) -> None:
        """Create a new cluster.

        The cluster will be bootstrapped if applicable.

        A bootstrapped cluster has a default namespace (`'default'`).

        Clusters persist their state.

        After initialization, services are started and ready.

        # TODO

        Should not start services but instead have a `run()` method that
        starts the cluster and serves its declared APIs.
        """
        if not isinstance(os.environ, EnvironLocal):
            os.environ = EnvironLocal()

        self.api_server = None
        self.host = host
        self.port = port
        self._publickeys = _read_key_files(service_account_key_file)
        self.deployments = {}
        self.pods = {}
        self.services = {}
        self.start()

    def start(self):
        """Start cluster.

        If the cluster has never been initialized, it will be
        bootstrapped.

        Services, watchers, and APIs are initialized and started.

        This method does not return.
        """
        with client() as self.etcd:
            self.start_apiserver()
            self.register_apiservice(self)
            self.start_watchers()
            if self.etcd.get(DEFAULT_NAMESPACE_KEY) == (None, None):
                self.bootstrap()
            self.start_deployments()
            # self.start_services()
            # self.start_pods()
            # self.start_ingress()

    def bootstrap(self) -> None:
        """Bootstrap cluster.

        Creates the initial resources, as defined in `coreapis.yaml`.
        Also creates a `'default'` namespace.

        If run on an already-initialized cluster, it will reset the
        default resources definitions.

        The `etcd` service is expected to be up and running.
        """
        for apiservice in yaml.safe_load_all(
            pkgutil.get_data('zabel.fabric', 'standalone/coreapis.yaml')
        ):
            groupversion = apiservice['groupVersion']
            if '/' in groupversion:
                group, version = groupversion.split('/')
            else:
                group, version = '', groupversion
            self.etcd.put(
                APISERVICE_KEY_TEMPLATE.format(group=group, version=version),
                json.dumps(apiservice),
            )
        try:
            self.create('namespaces', DEFAULT_NAMESPACE)
        except ValueError:
            pass

    # DNS proxy

    def dns_proxy(
        self, host: str, port: int, namespace: str
    ) -> Tuple[str, int]:
        """Resolve (host, port) in namespace.

        Services expose a name and a port and redirect the requests they
        receive to another address (and possibly another port).

        A service name is either a short name, a qualified name, or a
        fully qualified name:

            {my-service}
            {my-service}.{my-ns}
            {my-service}.{my-ns}.svc.cluster.local
        """
        if _is_dns_label(host):
            if (f'{host}.{namespace}', port) in self.services:
                return self.services[(f'{host}.{namespace}', port)]
        elif (host, port) in self.services:
            return self.services[(host, port)]
        return (host, port)

    # Controllers

    def start_apiserver(self) -> None:
        """Start the API server.

        The API server is started in a separate thread, running in
        normal mode (i.e., not in daemon mode).

        There is only one API server per cluster.
        """
        self.api_server = threading.Thread(
            target=default_app().run,
            kwargs={'host': self.host, 'port': self.port},
        )
        self.api_server.start()

    def register_apiservice(self, srv: ApiService) -> None:
        """Register an API service.

        The API service is connected to the API server, and receive the
        requests it can process.

        Any number of API services can be connected to the API server.

        In order to 'deregister' an API service, rebuild the router:

        app = bottle.app[0]
        # app.routes contains the routes list
        # app.router contains the router
        # must rebuild routes (and then router), in order to minimize
        # downtime (simple switch)
        for all apiservices:
            routes += ...
        router = bottle.Router()
        for route in routes:
            router.add(route.rule, route.method, route, name=route.name)
        app.router = router
        app.routes = routes
        """

        def wrap(handler, rbac: bool):
            def inner(*args, **kwargs):
                for header, value in DEFAULT_HEADERS.items():
                    response.headers[header] = value
                if rbac:
                    try:
                        user = self._ensure_authn()
                        self._ensure_authz(user)
                    except ValueError as err:
                        resp = err.args[0]
                        response.status = resp['code']
                        return resp
                self._ensure_admission()
                if request.query.limit:
                    kwargs['limit'] = request.query.limit
                if request.query.labelSelector:
                    kwargs['labelselector'] = request.query.labelSelector
                if request.query.fieldSelector:
                    kwargs['fieldselector'] = request.query.fieldSelector
                if request.json:
                    kwargs['body'] = request.json
                elif request.body:
                    body = request.body.read()
                    if body:
                        kwargs['body'] = yaml.safe_load(body)
                try:
                    result = json.dumps(handler(*args, **kwargs))
                    return result
                except ValueError as err:
                    resp = err.args[0]
                    response.status = resp['code']
                    return resp

            return inner

        for name in dir(srv):
            method = getattr(srv, name)
            for endpoint in getattr(method, 'entrypoint routes', []):
                default_app().route(
                    path=endpoint['path'].replace('{', '<').replace('}', '>'),
                    method=endpoint['methods'],
                    callback=wrap(method, endpoint['rbac']),
                )

    def start_watchers(self) -> None:
        """Start watches of interest."""
        self.etcd.add_watch_prefix_callback(DEPLOY_PREFIX, self.handle_deploy)
        self.etcd.add_watch_prefix_callback(CRD_PREFIX, self.handle_crd)
        self.etcd.add_watch_prefix_callback(POD_PREFIX, self.handle_pod)
        self.etcd.add_watch_prefix_callback(
            INGRESS_PREFIX, self.handle_ingress
        )
        self.etcd.add_watch_prefix_callback(SVC_PREFIX, self.handle_svc)

    def start_deployments(self) -> None:
        """Start deployments.

        Ensure deployments are up.  Used at cluster startup.
        """
        for namespace in self.list_allnamespaces('namespaces')['items']:
            _ns = namespace['metadata']['name']
            _deployments = self.list_namespaced('deployments', namespace=_ns)[
                'items'
            ]
            for deployment in _deployments:
                name = deployment['metadata']['name']
                fullname = f'{name}.{_ns}'
                if fullname not in self.deployments:
                    manifest = deployment['spec']['template']
                    pod_template_hash = _generate_hash(manifest)
                    pod_name = f'{name}-{pod_template_hash}'
                    try:
                        self.delete('pods', pod_name, namespace=_ns)
                    except ValueError:
                        pass
                    manifest['kind'] = 'Pod'
                    manifest['apiVersion'] = 'v1'
                    metadata = manifest['metadata']
                    metadata['name'] = pod_name
                    metadata['namespace'] = _ns
                    metadata['labels']['pod-template-hash'] = pod_template_hash
                    self.create('pods', manifest, namespace=_ns)
                    self.deployments[fullname] = pod_template_hash

    def handle_svc(self, event: Event) -> None:
        """Handle watch events for Services."""
        if isinstance(event, PutEvent):
            manifest = json.loads(event.value)
            namespace = manifest['metadata']['namespace']
            name = manifest['metadata']['name']
            for port in manifest['spec']['ports']:
                self.services[(f'{name}.{namespace}', port['port'])] = (
                    'localhost',
                    port.get('targetPort', port['port']),
                )
        else:
            manifest = json.loads(event.prev_value)
            namespace = manifest['metadata']['namespace']
            name = manifest['metadata']['name']
            for port in manifest['spec']['ports']:
                del self.services[(f'{name}.{namespace}', port['port'])]

    def handle_ingress(self, event: Event) -> None:
        """Handle watch events for Ingress."""
        if isinstance(event, PutEvent):
            manifest = json.loads(event.value)
            _ns = manifest['metadata']['namespace']
            rules = manifest['spec']['rules']
            http_paths = rules[0]['http']['paths']
            srvname = http_paths[0]['backend']['serviceName']
            path = http_paths[0]['path']
            if not path.endswith('/'):
                path += '/'
            # find Service
            _services = self.list_namespaced(
                'services',
                namespace=_ns,
                fieldselector=f'metadata.name=={srvname}',
            )['items']
            if not _services:
                ...  # wait for service to exist
            _service = _services[0]
            # find Pods
            selector = ','.join(
                f'{k}={v}' for k, v in _service['spec']['selector'].items()
            )
            _pods = self.list_namespaced(
                'pods', namespace=_ns, labelselector=selector
            )['items']
            if not _pods:
                ...  # wait for pod to exist
            pod = self.pods[f'{_pods[0]["metadata"]["name"]}.{_ns}']
            # mount
            default_app().mount(path, pod.app)

    def handle_crd(self, event: Event) -> None:
        """Handle watch events for CustomResourceDefinition."""
        if isinstance(event, PutEvent):
            manifest = json.loads(event.value)
            spec, grp = manifest['spec'], manifest['spec']['group']
            for ver in spec['versions']:
                key = APISERVICE_KEY_TEMPLATE.format(
                    group=grp, version=ver['name']
                )
                val, _ = self.etcd.get(key)
                if val is None:
                    val = APISERVICE_TEMPLATE.format(
                        group=grp, version=ver['name']
                    )
                apiservice = json.loads(val)
                for resource in apiservice['resources']:
                    if resource['name'] == spec['names']['plural']:
                        resource['singularName'] = spec['names']['singular']
                        resource['kind'] = spec['names']['kind']
                        # resource['shortNames'] = spec['names']['shortNames']
                        resource['namespaced'] = spec['scope'] == 'Namespaced'
                        break
                else:
                    apiservice['resources'].append(
                        {
                            'name': spec['names']['plural'],
                            'singularName': spec['names']['singular'],
                            'kind': spec['names']['kind'],
                            # 'shortNames': spec['names']['shortNames'],
                            'namespaced': spec['scope'] == 'Namespaced',
                            'verbs': [
                                'create',
                                'delete',
                                'deletecollection',
                                'get',
                                'list',
                                'patch',
                                'update',
                                'watch',
                            ],
                        }
                    )
                self.etcd.put(key, json.dumps(apiservice))
        else:
            ...

    def handle_pod(self, event: Event) -> None:
        """Handle Pod creation events."""

        def runner(image, env, args):
            ident = threading.current_thread().ident
            for var, value in env.items():
                os.environ[var] = value
            try:
                pod = image()
                self.pods[f'{name}.{_ns}'] = pod
                add_resolver(
                    ident, lambda host, port: self.dns_proxy(host, port, _ns)
                )
                self.update_status('pods', name, {'phase': 'Running'}, _ns)
                pod.run(*args)
                self.update_status('pods', name, {'phase': 'Succeeded'}, _ns)
            except Exception as err:
                self.update_status('pods', name, {'phase': 'Failed'}, _ns)
                print(err)
            finally:
                if get_resolver(ident):
                    remove_resolver(ident)
                del self.pods[f'{name}.{_ns}']

        if isinstance(event, PutEvent):
            if event.prev_value:
                return
            manifest = json.loads(event.value)
            name = manifest['metadata']['name']
            _ns = manifest['metadata']['namespace']
            self.update_status('pods', name, {'phase': 'Pending'}, _ns)
            try:
                threading.Thread(
                    target=runner, args=self._make_pod(manifest)
                ).start()
            except Exception as err:
                self.update_status('pods', name, {'phase': 'Failed'}, _ns)
                print(
                    f'Oops, something went wrong while starting pod {name} in namespace {_ns}: {err}'
                )

    def handle_deploy(self, event: Event) -> None:
        """Handle Deployment events.
        """
        if isinstance(event, PutEvent):
            deployment = json.loads(event.value)
            name = deployment['metadata']['name']
            _ns = deployment['metadata']['namespace']
            if event.prev_value:
                return
            pod = deployment['spec']['template']
            pod_template_hash = _generate_hash(pod)
            pod['kind'] = 'Pod'
            pod['apiVersion'] = 'v1'
            metadata = pod['metadata']
            metadata['name'] = f'{name}-{pod_template_hash}'
            metadata['namespace'] = _ns
            metadata['labels']['pod-template-hash'] = pod_template_hash
            self.create('pods', pod, namespace=_ns)
            self.deployments[f'{name}.{_ns}'] = pod_template_hash

    # Helpers

    def _get_env_value(
        self, definition: Dict[str, Any], namespace: str
    ) -> Optional[Union[str, Dict[str, Any]]]:
        if 'valueFrom' in definition:
            ref = definition['valueFrom']['secretKeyRef']
            secret = self.get('secrets', ref['name'], namespace=namespace)
            return str(base64.b64decode(secret['data'][ref['key']]), 'utf-8')
        return definition['value']

    def _make_pod(self, pod: Object) -> Any:
        _namespace = pod['metadata']['namespace']
        _container = pod['spec']['containers'][0]
        _modulename, _classname = _container['image'].rsplit('/', 1)
        _modulename = _modulename.replace('/', '.')
        _module = __import__(_modulename)
        for _name in _modulename.split('.')[1:]:
            _module = getattr(_module, _name)
        _image = getattr(_module, _classname)
        _env = {
            definition['name']: self._get_env_value(definition, _namespace)
            for definition in _container.get('env', [])
        }
        return _image, _env, _container.get('args', [])

    def _ensure_isnamespace(self, name: str) -> None:
        """Ensure the specified name is a known namespace.

        # Returned value

        None

        # Raised exception

        A _ValueError_ exception is raised if `name` is not a known
        namespace name.
        """
        namespace, _ = self.etcd.get(
            CLUSTER_KEY_TEMPLATE.format(resource='namespaces', name=name)
        )
        if namespace is None:
            raise ValueError(status('NotFound', f'Namespace {name} not found'))

    def _ensure_isplurals(self, name: str) -> str:
        """Ensure the specified name is known.

        # Returned value

        A string, the corresponding kind.

        # Raised exceptions

        A _ValueError_ exception is raised if `name` is not a known
        plurals name.
        """
        for resources, _ in self.etcd.get_prefix(APISERVICE_PREFIX):
            definitions = json.loads(resources)['resources']
            for resource in definitions:
                if name == resource['name']:
                    return resource['kind']
        raise ValueError(status('NotFound', f'{name} not found'))

    def _get_key(self, kind: str, name: str, namespace: str) -> str:
        if namespace is None:
            return CLUSTER_KEY_TEMPLATE.format(resource=kind, name=name)
        self._ensure_isnamespace(namespace)
        return NAMESPACED_KEY_TEMPLATE.format(
            resource=kind, namespace=namespace, name=name
        )

    def _ensure_authn(self) -> str:
        """Ensure the incoming request is authenticated.

        If from localhost, assume the `'localhost'` identity.

        If from somewhere else, use the subject value in the provided
        token.

        Raises a _ValueError_ exception if the token is missing or
        invalid, with the 'Unauthorized' flag set.
        """
        if request.remote_addr == '127.0.0.1':
            return 'localhost'
        authz = request.headers.get('Authorization')
        if authz is None:
            raise ValueError(status('Unauthorized', 'No Bearer token'))
        parts = authz.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            raise ValueError(
                status('Unauthorized', 'Invalid Authorization header')
            )
        try:
            return jwt.decode(parts[1], self._publickeys[0])['sub']
        except:
            raise ValueError(status('Unauthorized', 'Invalid token'))

    def _ensure_authz(self, user: str) -> None:
        """Ensure the incoming request is authorized.

        Raises a _ValueError_ exception if the request is not
        authorized, with the 'Forbidden' flag set.
        """
        if user in ('servicedesk', 'localhost') or ':' in user:
            return
        raise ValueError(status('Forbidden', 'Operation not allowed'))

    def _ensure_admission(self) -> None:
        pass

    # API

    # generic
    @entrypoint('/openapi/v2', methods=['GET'])
    def discover_openapi(self, **kwargs: Any) -> Dict[str, Any]:
        """Return the cluster's OpenAPI definitions."""
        return get_openapi(self)

    @entrypoint(API_ROUTE, methods=['GET'])
    def discover_api_versions(self, **kwargs: Any) -> Dict[str, Any]:
        """Describe cluster APIs."""
        return {
            'kind': 'APIVersions',
            'versions': ['v1'],
            'serverAddressByClientCIDRs': [
                {'clientCIDR': '0.0.0.0/0', 'serverAddress': 'localhost:8080'}
            ],
        }

    @entrypoint(APIGROUP_ROUTE, methods=['GET'])
    def discover_api_groups(self, **kwargs: Any) -> Object:
        """Describe available API groups."""
        versions = {
            yaml.safe_load(r)['groupVersion']
            for r, _ in self.etcd.get_prefix(APISERVICE_PREFIX)
        }
        return {
            'kind': 'APIGroupList',
            'apiVersion': 'v1',
            'groups': [
                {
                    'name': version.split('/')[0],
                    'versions': [
                        {
                            'groupVersion': version,
                            'version': version.split('/')[1],
                        }
                    ],
                    'preferredVersion': {
                        'groupVersion': version,
                        'version': version.split('/')[1],
                    },
                }
                for version in versions
                if '/' in version
            ],
        }

    @entrypoint(APISERVICE_ROUTES, methods=['GET'])
    def discover_api_resources(
        self, group: str = '', version: str = 'v1', **kwargs: Any
    ) -> Dict[str, Any]:
        """Describe available API resources."""
        apiservice, _ = self.etcd.get(
            APISERVICE_KEY_TEMPLATE.format(group=group, version=version)
        )
        return yaml.safe_load(apiservice)

    @entrypoint(CLUSTER_ROUTES, methods=['GET'])
    def list_allnamespaces(
        self,
        kind: str,
        labelselector: str = '',
        fieldselector: str = '',
        **kwargs: Any,
    ) -> Object:
        """Return a list of matching objects in all namespaces.

        Also used to returl list of cluster-level resources.

        # Required parameters

        - kind: a non-empty string

        # Optional parameters

        - labelselector: a string (empty by default)
        - fieldselector: a string (empty by default)

        # Returned value

        A dictionary with the following entries:

        - apiVersion: a string
        - kind: a string
        - items: a possibly empty list of dictionaries
        """
        _kind = self._ensure_isplurals(kind)
        prefix = CLUSTER_PREFIX_TEMPLATE.format(resource=kind)
        return make_items(
            _kind,
            [
                json.loads(obj)
                for obj, _ in self.etcd.get_prefix(prefix)
                if _match_label_selector(json.loads(obj), labelselector)
                and _match_field_selector(json.loads(obj), fieldselector)
            ],
        )

    @entrypoint(NAMESPACED_ROUTES, methods=['GET'])
    def list_namespaced(
        self,
        kind: str,
        namespace: str = DEFAULT_NAMESPACE_NAME,
        labelselector: str = '',
        fieldselector: str = '',
        **kwargs: Any,
    ) -> Object:
        """Return a list of objects matching kind and selectors.

        # Required parameters

        - kind: a non-empty string

        # Optional parameters

        - namespace: a non-empty string (default namespace by default)
        - labelselector: a string (empty by default)
        - fieldselector: a string (empty by default)

        # Returned value

        A dictionary with the following entries:

        - apiVersion: a string
        - kind: a string
        - items: a possibly empty list of dictionaries
        """
        self._ensure_isnamespace(namespace)
        _kind = self._ensure_isplurals(kind)
        prefix = NAMESPACED_PREFIX_TEMPLATE.format(
            resource=kind, namespace=namespace
        )
        return make_items(
            _kind,
            [
                json.loads(obj)
                for obj, _ in self.etcd.get_prefix(prefix)
                if _match_label_selector(json.loads(obj), labelselector)
                and _match_field_selector(json.loads(obj), fieldselector)
            ],
        )

    @entrypoint(DIRECT_ROUTES)
    def get(
        self,
        kind: str,
        name: str,
        namespace: Optional[str] = None,
        **kwargs: Any,
    ) -> Object:
        """Return the requested object.

        # Required parameters

        - kind: a non-empty string
        - name: a non-empty string

        # Optional parameters

        - namespace: a non-empty string or None (None by default)

        # Return value

        An object (a dictionary)
        """
        self._ensure_isplurals(kind)
        obj, meta = self.etcd.get(self._get_key(kind, name, namespace))
        if obj is None:
            raise ValueError(status('NotFound', f'Object {name} not found'))
        obj = json.loads(obj)
        obj['metadata']['resourceVersion'] = str(meta.mod_revision)
        return obj

    @entrypoint(CREATE_ROUTES)
    def create(
        self,
        kind: str,
        body: Object,
        namespace: Optional[str] = None,
        **kwargs,
    ) -> Object:
        """Create a new object.

        # Required parameters

        - body: a dictionary

        # Optional parameters

        - namespace: a non-empty string or None (None by default)

        If `namespace` is specified, it overrides the metadata.namespace
        value in `body`.

        # Returned value

        The created object (a dictionary).
        """
        _kind = self._ensure_isplurals(kind)
        if body['kind'] != _kind:
            raise ValueError(
                status(
                    'Invalid', f'Mismatched kinds: {_kind} and {body["kind"]}'
                )
            )
        metadata = body['metadata']
        name = metadata['name']

        key = self._get_key(kind, name, namespace)
        item, _ = self.etcd.get(key)
        if item is not None:
            raise ValueError(
                status('AlreadyExists', f'Object {name} already exists')
            )

        if namespace is not None:
            metadata['namespace'] = namespace
        metadata['creationTimestamp'] = datetime.datetime.now().isoformat()
        metadata['uid'] = str(uuid.uuid1())
        metadata['generation'] = 1
        body['status'] = {}

        self.etcd.put(key, json.dumps(body))

        return body

    @entrypoint(DIRECT_ROUTES)
    def update(
        self,
        kind: str,
        name: str,
        body: Object,
        namespace: Optional[str] = None,
        **kwargs: Any,
    ) -> Object:
        """Replace an existing object.

        # Required parameters

        - kind: a non-empty string
        - name: a non-empty string
        - body: a dictionary

        # Optional parameters

        - namespace: a non-empty string or None (None by default)

        # Returned value

        An object (a dictionary).
        """
        self._ensure_isplurals(kind)
        key = self._get_key(kind, name, namespace)
        obj, _ = self.etcd.get(key)
        if obj is None:
            raise ValueError(status('NotFound', f'Object {name} not found'))

        obj = json.loads(obj)
        if obj['metadata']['uid'] != body['metadata']['uid']:
            raise ValueError(status('Conflict', 'uid does not match'))
        if obj['metadata']['namespace'] != body['metadata']['namespace']:
            raise ValueError(status('Conflict', 'namespace does not match'))

        self.etcd.put(key, json.dumps(body))
        return body

    @entrypoint(DIRECT_ROUTES)
    def patch(
        self,
        kind: str,
        name: str,
        body: Object,
        namespace: Optional[str] = None,
        **kwargs: Any,
    ) -> Object:
        """Patch an existing object.

        # Required parameters

        - kind: a non-empty string
        - name: a non-empty string
        - body: a dictionary

        # Optional parameters

        - namespace: a non-empty string or None (None by default)

        If `namespace` is specified, it overrides the metadata.namespace
        value in `body`.

        # Returned value

        The patched object (a dictionary).
        """
        self._ensure_isplurals(kind)
        if 'generation' in body['metadata']:
            raise ValueError(status('Invalid', 'generation field in metadata'))

        key = self._get_key(kind, name, namespace)
        item, _ = self.etcd.get(key)
        if item is None:
            raise ValueError(status('NotFound', f'Object {name} not found'))

        obj = patchdict(json.loads(item), body)
        obj['metadata']['generation'] += 1
        self.etcd.put(key, json.dumps(obj))
        return obj

    @entrypoint(DIRECT_ROUTES)
    def delete(
        self, kind: str, name: str, namespace: Optional[str] = None, **kwargs,
    ) -> Object:
        """Delete an existing object.

        # Required parameters

        - kind: a non-empty string
        - name: a non-empty string

        # Optional parameters

        - namespace: a non-empty string or None (None by default)

        If `namespace` is not specified, it will delete the object in
        the default namespace.

        # Returned value

        The deleted object (a dictionary).
        """
        self._ensure_isplurals(kind)
        key = self._get_key(kind, name, namespace)
        obj, _ = self.etcd.get(key)
        if obj is None:
            raise ValueError(status('NotFound', f'Object {name} not found'))

        self.etcd.delete(key)
        return json.loads(obj)

    @entrypoint(STATUS_ROUTES, methods=['PATCH'])
    def patch_status(
        self,
        kind: str,
        name: str,
        body: Object,
        namespace: Optional[str] = None,
        **kwargs: Any,
    ) -> Object:
        pass

    @entrypoint(STATUS_ROUTES, methods=['UPDATE'])
    def update_status(
        self,
        kind: str,
        name: str,
        body: Object,
        namespace: Optional[str] = None,
        **kwargs: Any,
    ) -> Object:
        """Update an existing object status block."""
        key = self._get_key(kind, name, namespace)
        item, _ = self.etcd.get(key)
        if item is None:
            raise ValueError(status('NotFound', f'Object {name} not found'))
        obj = json.loads(item)
        obj['status'] = body
        self.etcd.put(key, json.dumps(obj))
        return obj

    @entrypoint(STATUS_ROUTES, methods=['GET'])
    def get_status(
        self,
        kind: str,
        name: Object,
        namespace: Optional[str] = None,
        **kwargs: Any,
    ) -> Object:
        pass
