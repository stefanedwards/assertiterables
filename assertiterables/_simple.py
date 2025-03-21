import pytest
from typing import Any, Dict, Tuple, cast

def is_iterable(x: Any | None) -> bool:
    """
    Tests whether `x` is an iterable, but *not* `str`, `bytes`, or `bytearray`.

    Other than this, 

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

def assert_is_iterable(x: Any | None):
    """
    Assert that `x` is an iterable, but *not* `str`, `bytes`, or `bytearray`.

    :param x:

    :raises pytest.fail.Exception:
        Raised when assertion fails.
    """
    if not is_iterable(x):
        pytest.fail("Object is not an iterable.")

def assert_is_single(container: Any | None) -> Any:
    """
    Assert that iterable `container` only contains a single element
    and returns that.

    .. warning::
        This method may iterate through any iterator or generator provided.
        I.e., this method has an **side effects** that the iterator's/generator's
        internal "position" may have shifted and a subsequent rewinding/resetting is 
        required!

    :param container:
        The iterable to test.

    :returns:
        A container, iterable, or generator that should contain exactly 1 element.

    :raises pytest.fail.Exception:
        Raised when assertion fails.
    
    Example::
        x = [ 5 ]
        itm = assert.iterable.assert_is_single(x)
        assert itm == 5
    """
    __tracebackhide__ = True
    assert_is_iterable(container)
    cont_ = cast(Any, container)

    itm = None
    length = 0
    has_exact_length = True
    if issubclass(type(cont_), dict):
        length,itm = _get_length_and_first_dict(cont_)
    else:
        try:
            length = len(cont_)
            if length > 0:
                itm = cont_[0]
        except TypeError:
            length,itm,has_exact_length = _get_length_and_first_iterable(cont_)
    
    if length == 0:
        pytest.fail("A single element was expected, but the iterable was empty.")
    elif length > 1:
        pytest.fail(f"A single element was expected, but the iterable contained {length if has_exact_length else f'{length} or more'} items.")
    
    return itm

def _get_length_and_first_dict(container: Dict[Any,Any]) -> Tuple[int,Any|None]:
    l = len(container)
    if l == 0:
        return (l, None)
    return (l, next(iter(container.items())))

def _get_length_and_first_iterable(container: Any) -> Tuple[int,Any|None,bool]:
    iterator = iter(container)
    try:
        itm = next(iterator)
    except StopIteration:
        return (0,None,True)
    try:
        _ = next(iterator)
    except StopIteration:
        return (1,itm,True)
    return (2,itm,False)


def assert_is_empty(container):
    """
    Assert that the iterable `container` contains exactly nothing.

    :param container:
        A container, iterable, or generator that should be empty.

    :raises pytest.fail.Exception:
        Raised when assertion fails.
    """
    __tracebackhide__ = True
    assert_is_iterable(container)
    cont_ = cast(Any, container)

    has_exact_length = True
    try:
        length = len(cont_)
    except TypeError:
        length,itm,has_exact_length = _get_length_and_first_iterable(cont_)

    if length > 0 and has_exact_length:
        pytest.fail(f"The iterable was expected to be empty, but it contained {length} items.")
    elif length > 0:
        pytest.fail(f"The iterable was not empty as expected.")
