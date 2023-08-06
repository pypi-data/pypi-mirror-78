# Copyright (c) 2019, 2020 Martin Lafaix (martin.lafaix@external.engie.com)
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0

"""
This module implements a naïve **etcd** service.

The public API it provides is a strict subset of the API offered by
the **python-etcd3** library.  Switching to it should be seamless. (The
opposite is not true, and not all features are implemented.)
"""


from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, Union

from datetime import datetime

import os
import pickle
import queue
import threading

########################################################################
########################################################################

# VData: data (bytes) with an attached revision number (int)
# HVData: when a key is deleted, its successive values (list of VData)
#         with an attached revision number (int)
# KVData: the 'life' of a key, with the list of changes of its current
#         incarnation (list of VData), as well as a list of its previous
#         incarnations (list of HVData).

# Finding the value of a key at a given time (revision) is as follows:
#
# If the revision is equal or higher than the revision of the initial
# current incarnation value, the value is the value of the change that
# has a revision that is lesser or equal to the desired revision.
#
# If the revision predates the revision of the initial current
# incarnation value, iterate over the previous incarnations, in
# decreasing order.  If the revision is higher or equal than the
# revision attached to the previous incarnation, the key had no value
# at the revision.  Otherwise proceed as in the current incarnation
# step.
#
# If no value is found, the key had no value at this revision.

VData = Tuple[bytes, int]  # data, revision
HVData = Tuple[List[VData], int]  # changes, revision
KVData = Tuple[List[VData], List[HVData]]  # changes, history

# Helpers

VALUE = 0
REVISION = 1


def _current(kvd: KVData, field: int) -> Any:
    return kvd[0][-1][field]


def _initial(kvd: KVData, field: int) -> Any:
    return kvd[0][0][field]


def _increment_last_byte(byte_string: bytes) -> bytes:
    array = bytearray(byte_string)
    array[-1] = array[-1] + 1
    return bytes(array)


def _to_bytes(maybe_bytestring: Union[str, bytes]) -> bytes:
    """Encode string to bytes.

    Convenience function to do a simple encode('utf-8') if the input is not
    already bytes. Returns the data unmodified if the input is bytes.
    """
    if isinstance(maybe_bytestring, bytes):
        return maybe_bytestring
    return maybe_bytestring.encode('utf-8')


# Events classes and helpers


class Event:
    """An event class for watchers.

    Do not use this class directly, use one of its subclass, #PutEvent
    and #DeleteEvent.
    """

    def __init__(
        self, key: bytes, value: Optional[bytes], prev_value: Optional[bytes]
    ) -> None:
        self.key = key
        self.value = value
        self.prev_value = prev_value

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.key!r}, {self.value!r}'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.key!r}, {self.value!r}>'


class PutEvent(Event):
    """Key creation or modification event."""


class DeleteEvent(Event):
    """Key deletion or expiration event."""


def _events_notifier(
    event_queue: queue.Queue,
    watchers: List[Tuple[bytes, bytes, Callable[..., None]]],
) -> None:
    while True:
        event = event_queue.get()
        for watcher in watchers:
            if not watcher:
                continue
            range_start, range_end, callback = watcher
            key = _to_bytes(event.key)
            if range_end is None:
                if key == range_start:
                    callback(event)
            elif range_start <= key < range_end:
                callback(event)


# Metadata class


class KVMetadata:
    """A container for key metadata."""

    def __init__(self, key: bytes, kv: KVData) -> None:
        self.key = key
        self.create_revision = _initial(kv, REVISION)
        self.mod_revision = _current(kv, REVISION)
        self.version = len(kv[0])
        self.lease_id = None

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}: {self.key!r}, version={self.version}'
        )

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.key!r}, version={self.version}>'


# EtcdClient class

WatcherEntry = Tuple[bytes, Optional[bytes], Callable[..., None]]


class EtcdClient:
    """An etcd-compatible implementation.

    The public API it provides is a strict subset of the API offered by
    the **python3-etcd** library.  Switching to it should be seamless.
    (The opposite is not true, as not all features are implemented.)

    `sort_order` is one of `'ascend`', `'descend'` or None.

    `sort_target` is one of `'key'`, `'version'`, `'create'`, `'mod'`,
    or `'value'`.

    Instances of this class can act as context managers:

    ```python
    with EtcdClient(...) as etcd:
        ...
    ```
    """

    store: Dict[bytes, KVData]
    revisions: Dict[int, datetime]
    revision: int

    def __init__(self, host: str = 'localhost', port: int = 2379):
        """..."""
        self._filename = f'{host}_{port}.pkl'
        if os.path.isfile(self._filename):
            with open(self._filename, 'rb') as f:
                self.revision, self.store, self.revisions = pickle.load(f)
        else:
            self.revision, self.store, self.revisions = 1, {}, {}
        self.watchers: List[Optional[WatcherEntry]] = []
        self.event_queue = queue.Queue()
        self.event_thread = threading.Thread(
            target=_events_notifier,
            args=[self.event_queue, self.watchers],
            daemon=True,
        )
        self.event_thread.start()

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self._filename}'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self._filename!r}>'

    ## Context manager helpers

    def __enter__(self) -> 'EtcdClient':
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    ## Revision helpers

    def _new_revision(self) -> int:
        self.revision += 1
        self.revisions[self.revision] = datetime.now()
        return self.revision

    ## Public API

    def close(self) -> None:
        """Snapshot and close the database."""
        self.snapshot()

    def snapshot(self, filename: Optional[str] = None) -> None:
        """Snapshot the database.

        # Optional parameters

        - filename: a non-empty string or None (None by default)
        """
        with open(filename or self._filename, 'wb') as f:
            pickle.dump(
                (self.revision, self.store, self.revisions),
                f,
                pickle.HIGHEST_PROTOCOL,
            )

    def get(self, key: bytes) -> Tuple[Optional[bytes], Optional[KVMetadata]]:
        """Get the value of a key.

        # Required parameters

        - key: a non-empty bytes string

        # Returned value

        A (value, metadata) tuple.  If `key` is not present, returns
        (None, None).
        """
        key = _to_bytes(key)

        if key not in self.store or not self.store[key][0]:
            return None, None
        kvb = self.store[key]
        return _current(kvb, VALUE), KVMetadata(key, kvb)

    def get_prefix(
        self,
        key_prefix: bytes,
        sort_order: Optional[str] = None,
        sort_target: str = 'key',
    ) -> Iterator[Tuple[bytes, KVMetadata]]:
        """Get a range of keys with a prefix.

        # Required parameters

        - key_prefix: a non-empty bytes string

        # Optional parameters

        - sort_target: a non-empty string or None (None by default)
        - sort_target: a non-empty string (`'key'` by default)

        # Returned value

        A sequence of (value, metadata) tuples.
        """
        key_prefix = _to_bytes(key_prefix)
        return self.get_range(
            key_prefix,
            _increment_last_byte(key_prefix),
            sort_order,
            sort_target,
        )

    def get_range(
        self,
        range_start: bytes,
        range_end: bytes,
        sort_order: Optional[str] = None,
        sort_target: str = 'key',
    ) -> Iterator[Tuple[bytes, KVMetadata]]:
        """Get a range of keys.

        # Required parameters

        - range_start: a non-empty bytes string
        - range_end: a non-empty bytes string

        # Returned value

        A sequence of (value, metadata) tuples.
        """
        keys = [
            k
            for k in self.store
            if range_start <= k < range_end and self.store[k][0]
        ]
        for k in keys:
            kvb = self.store[k]
            yield _current(kvb, VALUE), KVMetadata(k, kvb)

    def put(
        self, key: bytes, value: bytes, lease: int = 0, prev_kv: bool = False
    ) -> Optional[bytes]:
        """Save a value.

        # Required parameters

        - key: a non-empty bytes string
        - value: a bytes string

        # Optional parameters

        - lease: an integer (0 by default)
        - prev_kv: a boolean (False by default)
        """
        key = _to_bytes(key)
        value = _to_bytes(value)
        pair = (value, self._new_revision())

        kvb = self.store.get(key, ([], []))
        prev_value = _current(kvb, VALUE) if kvb[0] else None
        kvb[0].append(pair)
        self.store[key] = kvb
        event = PutEvent(key, value, prev_value)
        self.event_queue.put(event)
        return prev_value if prev_kv else None

    def delete(self, key: bytes, prev_kv: bool = False) -> bool:
        """Delete a single key.

        # Required parameters

        - key: a non-empty bytes string

        # Optional parameters

        - prev_kv: a boolean (False by default)

        # Returned values

        A boolean.  True if the deletion was successful, False
        otherwise.
        """
        key = _to_bytes(key)

        if key not in self.store or not self.store[key][0]:
            return False
        kvb = self.store[key]
        pair = (kvb[0], self._new_revision())
        self.store[key] = ([], kvb[1] + [pair])
        event = DeleteEvent(key, None, _current(kvb, VALUE))
        self.event_queue.put(event)
        return True

    def delete_prefix(self, prefix: bytes) -> int:
        """Delete a range of keys with a prefix.

        The operation is atomic, in the sense that all deleted keys are
        deleted at the same revision.

        # Required parameters

        - prefix: a non-empty bytes string

        # Returned value

        An integer, the number of deleted keys.
        """
        prefix = _to_bytes(prefix)

        keys = [
            k for k in self.store if k.startswith(prefix) and self.store[k][0]
        ]
        if not keys:
            return 0
        _revision = self._new_revision()
        values = []
        for k in keys:
            kvb = self.store[k]
            values.append(_current(kvb, VALUE))
            self.store[k] = ([], kvb[1] + [(kvb[0], _revision)])
        for k, value in zip(keys, values):
            self.event_queue.put(DeleteEvent(k, None, value))
        return len(keys)

    def replace(
        self, key: bytes, initial_value: bytes, new_value: bytes
    ) -> bool:
        """Atomically replace the value of a key with a new value.

        # Required parameters

        - key: a non-empty bytes string
        - initial_value: a bytes string
        - new_value: a bytes string

        # Returned value

        A boolean.  True if the replace operation was successful, False
        otherwise.
        """
        if self.get(key)[0] == initial_value:
            self.put(key, new_value)
            return True
        return False

    def add_watch_callback(
        self, key: bytes, callback: Callable[..., None], **kwargs: Any
    ) -> int:
        """Watch a key or range of keys and call a callback on every event.

        # Required parameters

        - key: a non-empty bytes string
        - callback: a function

        # Returned value

        An integer.  It can be used to cancel the watch.  Refer to
        #cancel_watch() for more information.
        """
        self.watchers.append(
            (_to_bytes(key), kwargs.get('range_end', None), callback)
        )
        return len(self.watchers)

    def add_watch_prefix_callback(
        self, key_prefix: bytes, callback: Callable[..., None], **kwargs: Any
    ) -> int:
        """Watch a prefix and call a callback on every event.

        # Required parameters

        - key_prefix: a non-empty bytes string
        - callback: a function

        # Returned value

        An integer.  It can be used to cancel the watch.  Refer to
        #cancel_watch() for more information.
        """
        kwargs['range_end'] = _increment_last_byte(_to_bytes(key_prefix))

        return self.add_watch_callback(key_prefix, callback, **kwargs)

    def cancel_watch(self, watch_id: int) -> None:
        """Stop watching a key or range of keys.

        # Required parameters

        - watch_id: an integer

        # Returned value

        None.
        """
        self.watchers[watch_id] = None

    def compact(self, revision: int) -> None:
        """Compact the event history up to a given revision.

        App superseded keys with a revision less than the compaction
        revision will be removed.
        """
        raise NotImplementedError


def client(host: str = 'localhost', port: int = 2379) -> EtcdClient:
    """Create a client."""
    return EtcdClient(host, port)
