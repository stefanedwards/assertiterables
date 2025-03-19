from typing import Any, Iterator
import pytest
from _pytest.outcomes import Failed
import collections as col
from assertiterables.iterables import is_iterable, assert_is_single, assert_is_empty, assert_is_iterable

# generator class for testing:
# does not have a __len__ property!
class my_iterator(object):
    class _iterator(object):
        def __init__(self, n: int):
            self.n = n
            self.num = 0

        def __next__(self):
            if self.num < self.n:
                cur, self.num = self.num, self.num+1
                return cur
            raise StopIteration()

    def __init__(self, n: int):
        self.n = n
    
    def __iter__(self):
        return my_iterator._iterator(self.n)

def my_generator(n: int) -> Iterator[int]:
    for i in range(n):
        yield i



def test_my_generator():
    assert list(my_iterator(2)) == [0, 1] # type: ignore
    # test that the object is stateless in regard to the returned iterator
    x = my_iterator(4)
    assert list(x) == [0, 1, 2, 3] # type: ignore
    assert list(x) == [0, 1, 2, 3] # type: ignore
    e = 0
    for i in my_iterator(3):
        assert e == i
        e += 1
    assert e == 3
    it = iter(x)
    assert next(it) == 0
    assert next(it) == 1
    assert next(it) == 2
    assert next(it) == 3
    with pytest.raises(BaseException) as excinfo:
        next(it)
    assert excinfo.typename == "StopIteration"




@pytest.mark.parametrize('x,outcome', [
    ('string', False),
    (None, False),
    (b'123', False),
    (bytearray([0, 1, 2]), False),
    (True, False),
    (False, False),
    (1, False),
    ([ ], True),
    (set(), True),
    (dict(), True),
    (my_iterator(4), True)
])
def test_is_iterable(x, outcome):
    assert is_iterable(x) == outcome

    if outcome == False:
        with pytest.raises(Failed, match="Object is not an iterable."):
            assert_is_iterable(x)

@pytest.mark.parametrize('x', [
    'string',
    None,
    b'123',
    bytearray([0, 1, 2]),
    True,
    False,
    1,
])
def test_single_bad_objects(x):
    with pytest.raises(Failed, match = "Object is not an iterable."):
        assert_is_single(x)

    with pytest.raises(Failed, match="Object is not an iterable."):
        assert_is_empty(x)

@pytest.mark.parametrize('x', [
   tuple(),
   set(),
   list(),
   dict(),
   my_iterator(0)
])
def test_single_empty_objects(x):
    with pytest.raises(Failed, match="A single element was expected, but the iterable was empty."):
        assert_is_single(x)
    assert_is_empty(x)


@pytest.mark.parametrize('x', [
   (1,2),
   set([1,2]),
   ['a', 3],
   { 'a': 3, 'b': 4 },
   range(3)
])
def test_single_not_singular(x):
    with pytest.raises(Failed, match=
        "A single element was expected, but the iterable contained ([1-9]+)( or more)? items\\."):
        assert_is_single(x)

    with pytest.raises(Failed, match=
        "The iterable was expected to be empty, but it contained ([1-9]+) items."):
        assert_is_empty(x)


@pytest.mark.parametrize('x', [
    range(0),
    my_iterator(0),
    my_generator(0),
])
def test_single_empty_iterable(x):
    with pytest.raises(Failed, match="A single element was expected, but the iterable was empty."):
        assert_is_single(x)
    assert_is_empty(x)

@pytest.mark.parametrize('x', [
    range(1),
    my_iterator(1),
])
def test_single_generator_range1(x: Any):
    assert 0 == assert_is_single(x)
    with pytest.raises(Failed, match=
        "The iterable was expected to be empty, but it contained 1 items."):
        assert_is_empty(x)


def test_single_generator_my_generator1():
    x = my_generator(1)
    assert 0 == assert_is_single(x)
    ## reset generator
    x = my_generator(1)
    with pytest.raises(Failed, match=
        "The iterable was expected to be empty, but it contained 1 items."):
        assert_is_empty(x)

def test_single_generator_my_generator2():
    x = my_generator(2)
    with pytest.raises(Failed, match=
        'A single element was expected, but the iterable contained 2 or more items.'):
        assert 0 == assert_is_single(x)

    ## reset generator
    x = my_generator(3)
    with pytest.raises(Failed, match=
        "The iterable was not empty as expected."):
        assert_is_empty(x)

def test_empty_generator_my_generator1():
    x = my_generator(0)
    with pytest.raises(Failed, match=
        "A single element was expected, but the iterable was empty.") as excinfo:
        assert 0 == assert_is_single(x)
    ## reset generator
    x = my_generator(0)
    assert_is_empty(x)
    

@pytest.mark.parametrize('x,expected', [
   ((1,), 1),
   (set([2]), 2),
   (['c'], 'c'),
   ({ 'd': 4 }, ('d',4)),
])
def test_single_singular(x, expected):
    itm = assert_is_single(x)
    assert itm == expected

    with pytest.raises(Failed, match=
        "The iterable was expected to be empty, but it contained 1 items."):
        assert_is_empty(x)

# test more advanced types from collections
def test_single_collections():
    # doesn't make sense, but it works
    Point = col.namedtuple("Point", ["x", "y"])
    p = Point(11, y = 22)
    test_single_not_singular(p)
    # also senseless
    OneDimension = col.namedtuple("OneDimension", ["x"])
    od = OneDimension(4)
    test_single_singular(od, 4)
    # more nonsense
    ZeroDimension = col.namedtuple("ZeroDimension", [ ])
    test_single_empty_objects(ZeroDimension())

    # better example
    d = col.deque('ghi')
    test_single_not_singular(d)
    e = col.deque('j')
    test_single_singular(e, 'j')


