# Copyright (c) 2020 Martin Lafaix (martin.lafaix@external.engie.com)
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0

"""
This module implements a thread-specific DNS resolver.

The DNS resolver performs the translation from one `name`:`port` pair to
another `targetname`:`targetPort` pair.  The translation is
thread-specific.

`name` and `targetname` can be IP addresses (but does not have to).

DNS requests performed using the **requests** library (or any other
python library that rely on the **socket** library) will be passed
to the specified resolver.
"""

from typing import Any, Callable, List, Optional, Tuple

import socket
import threading

thread_cache = {}


def add(ident: int, resolver: Callable[[str, int], Tuple[str, int]]) -> None:
    """Set the thread resolver.

    The `resolver` function takes two arguments: a string and an
    integer and returns a (string, int) tuple.

    # Required parameters

    - ident: an integer (the thread ident)
    - resolver: a function

    # Returned value

    None.
    """
    thread_cache[ident] = resolver


def get(ident: int) -> Optional[Callable[[str, int], Tuple[str, int]]]:
    """Return the current thread resolver.

    # Required parameters

    - ident: an integer (the thread ident)

    # Returned value

    The current resolver or None if none were set.
    """
    return thread_cache.get(ident)


def remove(ident: int) -> None:
    """Reset the thread resolver.

    # Required parameters

    - ident: an integer (the thread ident)

    # Returned value

    None.

    # Raised exception

    A _KeyError_ exception is raised if no thread resolver has been set
    for the specified thread.
    """
    del thread_cache[ident]


# Inspired by: https://stackoverflow.com/a/15065711/868533
_prv_getaddrinfo = socket.getaddrinfo


def _new_getaddrinfo(*args):
    # Uncomment to see what calls to `getaddrinfo` look like.
    # print('args', args)
    try:
        override = thread_cache[threading.current_thread().ident](*args[:2])
        return _prv_getaddrinfo(*override, *args[2:])
    except KeyError:
        return _prv_getaddrinfo(*args)


socket.getaddrinfo = _new_getaddrinfo
