import pytest
from typing import Any, Dict, Tuple, cast
from warnings import warn

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
    for expected in args:
        try:
            actual = next(iterator)
        except StopIteration:
            break
        container_count += 1

        if callable(expected):
            if expected.__code__.co_argcount != 1:
                raise ValueError("All positional arguments to `assert_collection` must either be callable with exactly 1 argument or an object to compare.")
            pytest.raises
            expected(actual)
        else:
            pass







class AssertCollectionException(pytest.fail.Exception):
    pass

# Contains Subset Assertion: checks whether a set contains another set as a subset.

# assert subset <= full_set