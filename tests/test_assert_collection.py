import pytest
from _pytest.outcomes import Failed
import warnings
from assertiterables import assert_is_iterable
from assertiterables import assert_collection, assert_all, AssertCollectionException

def test_single_match_object():
    obj = [ 1 ]

    assert_collection(obj, 1)
    assert_collection(obj, lambda x: (
        x == 1
    ))

    with pytest.raises(AssertCollectionException, match="Index 0 failed test."):
        assert_collection(obj, 2)
    with pytest.raises(AssertCollectionException, match="Index 0 failed test."):
        assert_collection(obj, lambda x: x is None)

    assert_all(obj, 1)
    assert_all(obj, lambda x: (
        x == 1
    ))

    with pytest.raises(AssertCollectionException, match="Index 0 failed test."):
        assert_all(obj, 2)
    with pytest.raises(AssertCollectionException, match="Index 0 failed test."):
        assert_all(obj, lambda x: x is None)


def test_too_short_iterable():
    obj = [ 1, 2]
    assert_collection(obj, 1, 2)

    with pytest.raises(AssertCollectionException, match="Expected 3 elements, got only 2."):
        assert_collection(obj, 1, 2, 3)

def test_too_long_iterable():
    obj = [1, 2, 3, 4]
    assert_collection(obj, 1, 2, 3, 4)

    with pytest.raises(AssertCollectionException, match="Expected 2 elements, got 3 or more."):
        assert_collection(obj, 1, 2)


def test_partial_failure():
    obj = [1, 2, 3, 4]

    with pytest.raises(AssertCollectionException, match="Only 2/4 elements passed their tests."):
        assert_collection(obj, 2, 3, 3, 4)
    with pytest.raises(AssertCollectionException, match="Only 2/4 elements passed their tests."):
        assert_all(obj, lambda x: x < 3)

def test_mixed_bag():
    obj = range(3)
    with pytest.raises(AssertCollectionException, match="All 3 elements failed their tests.") as excinfo:
        assert_collection(obj, 
            lambda x: x == 1,
            2,
            assert_is_iterable)
    assert all((not passed for passed in excinfo.value.passed))
    assert_all(excinfo.value.passed, False)

    assert_collection(excinfo.value.results,
        None, lambda x: None, lambda x: issubclass(type(x), Failed))

def test_empty_collection():
    with warnings.catch_warnings(record=True) as w:
        assert_collection(list())
        assert str(w[0].message) == "Use `assert_is_empty` instead of `assert_collection` with an empty argument set."
        assert w[0].category == UserWarning
    
    with pytest.raises(Failed):
        with warnings.catch_warnings(record=True) as w:
            assert_collection([1, 2])
            assert str(w[0].message) == "Use `assert_is_empty` instead of `assert_collection` with an empty argument set."
            assert w[0].category == UserWarning

def test_bad_signature():
    def foo(bar, zoo):
        return True
    
    with pytest.raises(ValueError, match="All positional arguments to `assert_collection` must either be callable with exactly 1 argument or an object to compare.") as excinfo:
        assert_collection([ 1 ], foo)
    with pytest.raises(ValueError, match="All positional arguments to `assert_collection` must either be callable with exactly 1 argument or an object to compare.") as excinfo:
        assert_all([ 1 ], foo)

def test_failed_lambda():
    ## The lambda statement does not support assert statements.
    ## To use assert, it has to be wrapped in a separate function

    def foo(x):
        assert x == 1

    with pytest.raises(AssertCollectionException) as excinfo:
        assert_all(range(2), foo)
    assert_collection(excinfo.value.results, 
        AssertionError,
        None)
    #assert type(excinfo.value.results[0]) == AssertionError
    #assert excinfo.value.results[1] 


def test_AssertCollectionException():
    exc = AssertCollectionException([True], [True])
    assert str(exc) == "All elements passed. A fault must exist somewhere else."