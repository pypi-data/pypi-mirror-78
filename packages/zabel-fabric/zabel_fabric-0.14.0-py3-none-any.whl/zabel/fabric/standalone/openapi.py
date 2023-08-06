# Copyright (c) 2019, 2020 Martin Lafaix (martin.lafaix@external.engie.com)
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0

"""
**zabel** openapi helper."""

import yaml

BOILERPLATE = {
    "swagger": "2.0",
    "openapi": "3.0.3",
    "info": {"title": "Zabel", "version": "0.10.0"},
    "paths": {
        "/api/": {
            "get": {
                "description": "get available API versions",
                "consumes": ["application/json",],
                "produces": ["application/json",],
                "schemes": ["https"],
                "tags": ["core"],
                "operationId": "getCoreAPIVersions",
                "responses": {
                    "200": {"description": "OK",},
                    "401": {"description": "Unauthorized"},
                },
            }
        },
        "/api/v1/": {
            "get": {
                "description": "get available resources",
                "consumes": ["application/json",],
                "produces": ["application/json",],
                "schemes": ["https"],
                "tags": ["core_v1"],
                "operationId": "getCoreV1APIResources",
                "responses": {
                    "200": {"description": "OK",},
                    "401": {"description": "Unauthorized"},
                },
            }
        },
    },
}

BASE_GROUP = {
    "description": "get information of a group",
    "consumes": ["application/json",],
    "produces": ["application/json",],
    "schemes": ["https"],
    "tags": ["{group}"],
    "operationId": "get{Group}APIGroup",
    "responses": {
        "200": {"description": "OK",},
        "401": {"description": "Unauthorized"},
    },
}


BASE_RESOURCES = {
    "description": "get available resources",
    "consumes": ["application/json",],
    "produces": ["application/json",],
    "schemes": ["https"],
    "tags": ["{group}_{version}"],
    "operationId": "get{Group}{Version}APIResources",
    "responses": {
        "200": {"description": "OK",},
        "401": {"description": "Unauthorized"},
    },
}

BASE_CREATE_PARAMETERS = [
    {"name": "body", "in": "body", "required": True,},
    {
        "uniqueItems": True,
        "type": "string",
        "description": "When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed",
        "name": "dryRun",
        "in": "query",
    },
    {
        "uniqueItems": True,
        "type": "string",
        "description": "fieldManager is a name associated with the actor or entity that is making these changes. The value must be less than or 128 characters long, and only contain printable characters, as defined by https://golang.org/pkg/unicode/#IsPrint.",
        "name": "fieldManager",
        "in": "query",
    },
]

BASE_LIST_PARAMETERS = [
    {
        "uniqueItems": True,
        "type": "string",
        "description": "The continue option should be set when retrieving more results from the server. Since this value is server defined, clients may only use the continue value from a previous query result with identical query parameters (except for the value of continue) and the server may reject a continue value it does not recognize. If the specified continue value is no longer valid whether due to expiration (generally five to fifteen minutes) or a configuration change on the server, the server will respond with a 410 ResourceExpired error together with a continue token. If the client needs a consistent list, it must restart their list without the continue field. Otherwise, the client may send another list request with the token received with the 410 error, the server will respond with a list starting from the next key, but from the latest snapshot, which is inconsistent from the previous list results - objects that are created, modified, or deleted after the first list request will be included in the response, as long as their keys are after the \"next key\".\n\nThis field is not supported when watch is true. Clients may start a watch from the last resourceVersion value returned by the server and not miss any modifications.",
        "name": "continue",
        "in": "query",
    },
    {
        "uniqueItems": True,
        "type": "string",
        "description": "A selector to restrict the list of returned objects by their fields. Defaults to everything.",
        "name": "fieldSelector",
        "in": "query",
    },
    {
        "uniqueItems": True,
        "type": "string",
        "description": "A selector to restrict the list of returned objects by their labels. Defaults to everything.",
        "name": "labelSelector",
        "in": "query",
    },
    {
        "uniqueItems": True,
        "type": "integer",
        "description": "limit is a maximum number of responses to return for a list call. If more items exist, the server will set the `continue` field on the list metadata to a value that can be used with the same initial query to retrieve the next set of results. Setting a limit may return fewer than the requested amount of items (up to zero items) in the event all requested objects are filtered out and clients should only use the presence of the continue field to determine whether more results are available. Servers may choose not to support the limit argument and will return all of the available results. If limit is specified and the continue field is empty, clients may assume that no more results are available. This field is not supported if watch is true.\n\nThe server guarantees that the objects returned when using continue will be identical to issuing a single list call without a limit - that is, no objects created, modified, or deleted after the first request is issued will be included in any subsequent continued requests. This is sometimes referred to as a consistent snapshot, and ensures that a client that is using limit to receive smaller chunks of a very large result can ensure they see all possible objects. If objects are updated during a chunked list the version of the object that was present at the time the first list result was calculated is returned.",
        "name": "limit",
        "in": "query",
    },
    {
        "uniqueItems": True,
        "type": "string",
        "description": "When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. When specified for list: - if unset, then the result is returned from remote storage based on quorum-read flag; - if it's 0, then we simply return what we currently have in cache, no guarantee; - if set to non zero, then the result is at least as fresh as given rv.",
        "name": "resourceVersion",
        "in": "query",
    },
    {
        "uniqueItems": True,
        "type": "integer",
        "description": "Timeout for the list/watch call. This limits the duration of the call, regardless of any activity or inactivity.",
        "name": "timeoutSeconds",
        "in": "query",
    },
    {
        "uniqueItems": True,
        "type": "boolean",
        "description": "Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion.",
        "name": "watch",
        "in": "query",
    },
]

VERB_OPERATION = {
    'list': 'get',
    'create': 'post',
    'deletecollection': 'delete',
    'delete': 'delete',
    'get': 'get',
    'patch': 'patch',
    'update': 'put',
}

GENERIC_VERBS = {'list', 'create', 'deletecollection'}
SPECIFIC_VERBS = {'delete', 'get', 'patch', 'update'}

PREFIX = b'/registry/apiregistration.k8s.io/apiservices/'


def _emit_generics(resource, context):
    return {
        VERB_OPERATION[verb]: _emit_operation(verb, resource, context)
        for verb in GENERIC_VERBS & set(resource['verbs'])
    }


def _emit_specifics(resource, context):
    return {
        VERB_OPERATION[verb]: _emit_operation(verb, resource, context)
        for verb in SPECIFIC_VERBS & set(resource['verbs'])
    }


def _emit_operation(verb, resource, context):
    namespaced = 'Namespaced' if resource.get('namespaced') else ''
    return {
        'description': f'{verb} objects of kind {resource["kind"]}',
        'consumes': ['*/*'],
        'produces': ['application/json'],
        'tags': [context['tag']],
        'operationId': f'{verb}{context["baseoperation"]}{namespaced}{resource["kind"]}',
        'responses': {
            '200': {'description': 'OK'},
            '401': {'description': 'Unauthorized'},
        },
    }


def _emit_subresource(root, resource, context):
    res, sub = resource['name'].split('/')
    if resource.get('namespaced'):
        path = f'{root}/namespaces/{{namespace}}/{res}/{{name}}/{sub}'
    else:
        path = f'{root}/{res}/{{name}}/{sub}'
    verbs = set(resource['verbs'])
    if GENERIC_VERBS & verbs:
        raise ValueError('oops, got generic verb for subresource')
    BOILERPLATE['paths'][path] = _emit_specifics(resource, context)


def _emit_resource(root, resource, context):
    if resource.get('namespaced'):
        path = f'{root}/namespaces/{{namespace}}/{resource["name"]}'
    else:
        path = f'{root}/{resource["name"]}'
    verbs = set(resource['verbs'])
    if GENERIC_VERBS & verbs:
        BOILERPLATE['paths'][path] = _emit_generics(resource, context)
    if SPECIFIC_VERBS & verbs:
        BOILERPLATE['paths'][f'{path}/{{name}}'] = _emit_specifics(
            resource, context
        )


def _ensure_emit_group(groupversion, context):
    group, _ = groupversion.split('/')
    key = f'/apis/{group}/'
    if key not in BOILERPLATE['paths']:
        name = group.split('.')[0] if group.endswith('.k8s.io') else group
        information = BASE_GROUP.copy()
        information['tags'] = [name.lower()]
        information['operationId'] = f'get{context["baseoperation"]}ApiGroup'
        BOILERPLATE['paths'][key] = {'get': information}


def _emit_group_version(root, context):
    resources = BASE_RESOURCES.copy()
    resources['tags'] = [context['tag']]
    resources['operationId'] = f'get{context["baseoperation"]}APIResources'
    BOILERPLATE['paths'][f'{root}/'] = {'get': resources}


def _make_tag(groupversion: str) -> str:
    """Make tag corresponding to groupversion."""
    if '/' in groupversion:
        group, version = groupversion.split('/')
        splits = group.split('.')
        lhs = splits[0].lower() + ''.join(s.title() for s in splits[1:])
        return f'{lhs}_{version.lower()}'
    return f'core_{groupversion.lower()}'


def _make_operationname(groupversion: str) -> str:
    """Make CamelCase base operation name."""
    if '/' in groupversion:
        group, version = groupversion.split('/')
        if group.endswith('.k8s.io'):
            group = group[:-7]
        return ''.join(s.title() for s in group.split('.')) + version.title()
    return f'Core{groupversion.title()}'


def get_openapi(cluster):
    """Generate a JSON swagger for the specified cluster.

    Entries will be generated for each declared apiservices.
    """
    apis = [yaml.safe_load(r) for r, _ in cluster.etcd.get_prefix(PREFIX)]

    for api in apis:
        groupversion = api['groupVersion']
        context = {
            'tag': _make_tag(groupversion),
            'baseoperation': _make_operationname(groupversion),
        }
        if '/' in groupversion:
            root = f'/apis/{groupversion}'
            _ensure_emit_group(groupversion, context)
            _emit_group_version(root, context)
        else:
            root = f'/api/{groupversion}'

        for resource in api['resources']:
            if '/' in resource['name']:
                _emit_subresource(root, resource, context)
            else:
                _emit_resource(root, resource, context)
    return BOILERPLATE
