# SPDX-FileCopyrightText: 2025-present Stefan McKinnon Edwards <sme@iysik.com>
#
# SPDX-License-Identifier: MIT

from .__about__ import __version__, version_tuple
from ._simple import assert_is_empty, assert_is_iterable, assert_is_single, is_iterable
from .assert_collection import assert_collection, AssertCollectionException

__all__ = [
    "AssertCollectionException",
    "assert_collection",
    "assert_is_empty",
    "assert_is_iterable",
    "assert_is_single",
    "is_iterable",
    "__version__",
    "version_tuple",
]