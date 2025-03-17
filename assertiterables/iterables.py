import pytest
from typing import Any, List


def is_iterable(x: Any | None) -> bool:
    """
    Tests whether `x` is an iterable, but *not* `str`, `bytes`, or `bytearray`.

    :param x:
        The object to test.

    :returns:
        Boolean value.
    """
    if x is None:
        return False
    t = type(x)
    if issubclass(t, str) or issubclass(t, bytes) or issubclass(t, bytearray):
        return False
    try:
        iter(x)
        return True
    except:
        return False

def single(container: Any | None) -> Any:
    """Assert that iterable `container` only contains a single element
    and returns that.

    :param x:
        The iterable to test.

    :returns:
        The single element, if it is the only element.

    :raises pytest.fail.Exception:
        Raised when assertion fails.
    
    Example::
        x = [ 5 ]
        itm = assert.iterable.single(x)
        assert itm == 5
    """
    __tracebackhide = True
    if not is_iterable(container):
        pytest.fail("Object is not an iterable.")
    if len(container) == 0:
        pytest.fail("A single element was expected, but the iterable was empty.")
    elif len(container) > 1:
        pytest.fail(f"A single element was expected, but the iterable contained {len(container)} items.")
    return container[0]

def empty(container):
    assert not container

# Contains Subset Assertion: checks whether a set contains another set as a subset.

# assert subset <= full_set