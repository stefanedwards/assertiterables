from typing import Any, List, Dict, cast
from warnings import warn
import pytest
from _pytest.outcomes import OutcomeException
from assertiterables import assert_is_empty, assert_is_iterable

def assert_collection(container, *args):
    """
    Assert each item in a collection separately.

    :param container:
        A container, iterable, or generator to test.

    .. warning::
        **NB!** This method may iterate through any iterator or generator provided.
        I.e., this method has an **side effects** that the iterator's/generator's
        internal "position" may have shifted and a subsequent rewinding/resetting is 
        required!
    
    :raises pytest.fail.Exception:
        Raised when assertion fails.
    """
    __tracebackhide__ = True
    assert_is_iterable(container)
    cont_ = cast(Any, container)

    if len(args) == 0:
        warn("Use `assert_is_empty` instead of `assert_collection` with an empty argument set.", 
             category=UserWarning)
        assert_is_empty(container)
        return

    container_count = 0
    iterator = iter(container)
    passed = [False]*len(args)
    results: List[Any | None] = [None]*len(args)
    for expected in args:
        try:
            actual = next(iterator)
        except StopIteration:
            break
        container_count += 1

        if callable(expected):
            if expected.__code__.co_argcount != 1:
                raise ValueError("All positional arguments to `assert_collection` must either be callable with exactly 1 argument or an object to compare.")
            try:
                result = expected(actual)
                if result is None or result is not False:
                    passed[container_count] = True
                    results[container_count] = result
            except (OutcomeException,AssertionError) as e:
                results[container_count] = e
            finally:
                continue
        else:
            passed[container_count] = actual == expected 
    








class AssertCollectionException(pytest.fail.Exception):
    pass

# Contains Subset Assertion: checks whether a set contains another set as a subset.

# assert subset <= full_set