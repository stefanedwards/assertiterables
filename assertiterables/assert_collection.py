from typing import Any, List, Dict, Callable, Iterable
from warnings import warn
from _pytest.outcomes import OutcomeException,Failed
from assertiterables import assert_is_empty, assert_is_iterable


def assert_collection(container: Iterable, *args: object | Callable | None):
    """
    Assert each item in a collection separately.

    :param container:
        A container, iterable, or generator to test.

    .. warning::
        **NB!** This method may iterate through any iterator or generator provided.
        I.e., this method has an **side effects** that the iterator's/generator's
        internal "position" may have shifted and a subsequent rewinding/resetting is 
        required!
    
    :raises _pytest.outcomes.Failed:
        Raised when assertion fails.

    Example::
        assert_collection(range(3),
            lambda x: x == 0,
            lambda x: x < 3,
            lambda x: issubclass(type(x), int))
    """
    __tracebackhide__ = True
    assert_is_iterable(container)

    if len(args) == 0:
        warn("Use `assert_is_empty` instead of `assert_collection` with an empty argument set.", 
             category=UserWarning)
        assert_is_empty(container)
        return
    
    container_count = -1
    iterator = iter(container)
    passed: List[bool] = [False]*len(args)
    results: List[Any | None] = [None]*len(args)
    for expected in args:
        try:
            actual = next(iterator)
        except StopIteration:
            break
        container_count += 1

        passed[container_count],results[container_count] = _assert_item(actual, expected)

    container_count += 1

    if container_count < len(args):
        raise AssertCollectionException(passed, results, {
            "error": "iterable too short",
            "container": container_count,
            "args": len(args)
        })
    
    try:
        next(iterator)
        raise AssertCollectionException(passed, results, {
            "error": "too few arguments",
            "container": container_count+1,
            "args": len(args)
        })
    except StopIteration:
        pass

    if not all(passed):
        raise AssertCollectionException(passed, results)



class AssertCollectionException(Failed):
    def __init__(self, passed: List[bool], results: List[Any | None], extras: Dict[str, Any] | None = None):
        self.passed = passed
        self.results = results
        self.extras = extras
        self.pytrace = True
    
    # TODO: Provide more details on failures.
    @property
    def msg(self) -> str: # type: ignore
        if self.extras is not None and self.extras["error"] == "iterable too short":
            return f"Expected {self.extras['args']} elements, got only {self.extras['container']}."
        
        if self.extras is not None and self.extras["error"] == "too few arguments":
            return f"Expected {self.extras['args']} elements, got {self.extras['container']} or more."

        failure_count = sum((not passed for passed in self.passed))
        if failure_count == 0:
            return "All elements passed. A fault must exist somewhere else."
        if failure_count == 1:
            return f"Index {self.passed.index(False)} failed test."
        if failure_count < len(self.passed):
            return f"Only {(len(self.passed)-failure_count)}/{len(self.passed)} elements passed their tests."
        if failure_count == len(self.passed):
            return f"All {len(self.passed)} elements failed their tests."


def _assert_item(actual, expected):
    if type(expected) is type:
        return (isinstance(type(actual), type), {"actual": actual, "expected": expected}) 
    elif callable(expected):
        if expected.__code__.co_argcount != 1:
            raise ValueError("All positional arguments to `assert_collection` must either be callable with exactly 1 argument or an object to compare.")
        try:
            result = expected(actual)
            if result is False:
                return (False, None)
            return (True, result)
        except (OutcomeException,AssertionError) as e:
            return (False, e)
    else:
        return (actual == expected, {"actual": actual, "expected": expected}) 

def assert_all(container: Iterable, expected: object | Callable | None):
    """
    Assert **all** elements of an iterable.

    :param container:
        A container, iterable, or generator to test.

    .. warning::
        **NB!** This method may iterate through any iterator or generator provided.
        I.e., this method has an **side effects** that the iterator's/generator's
        internal "position" may have shifted and a subsequent rewinding/resetting is 
        required!
    
    :raises _pytest.outcomes.Failed:
        Raised when assertion fails.

    """
    __tracebackhide__ = True
    assert_is_iterable(container)

    passed,results = zip(*(_assert_item(itm, expected) for itm in container))
    if sum(passed) < len(passed):
        raise AssertCollectionException(passed, results)


# Contains Subset Assertion: checks whether a set contains another set as a subset.

# assert subset <= full_set