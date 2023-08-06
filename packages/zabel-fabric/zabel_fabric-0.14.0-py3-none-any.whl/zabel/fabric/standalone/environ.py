# Copyright (c) 2020 Martin Lafaix (martin.lafaix@external.engie.com)
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0

"""
This module provides a thread-local `os.environ`.
"""

import os
import threading

REFERENCE_ENVIRON = os.environ


class EnvironLocal(threading.local):
    """A thread-local copy of `os.environ`.

    The provided copy of `os.environ` only offers a 'dict-like'
    interface.
    """

    def __init__(self):
        for var, value in REFERENCE_ENVIRON.items():
            self.__dict__[var] = value

    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)

    def __setitem__(self, key, value):
        self.__dict__.__setitem__(key, value)

    def __contains__(self, key):
        return key in self.__dict__

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def items(self):
        return self.__dict__.items()

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return self.__dict__.__iter__()
