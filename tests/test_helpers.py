from typing import Any, Iterator
import pytest

from assertiterables.helpers import _len


# generator class for testing:
# does not have a __len__ property!
class my_iterable(object):
    def __init__(self, n: int):
        self.n = n
        self.num = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    
    def next(self):
        if self.num < self.n:
            cur, self.num = self.num, self.num+1
            return cur
        raise StopIteration()
    
def my_generator(n: int) -> Iterator[int]:
    for i in range(n):
        yield i
    
@pytest.mark.parametrize('x,max_try,expected_bool,expected_length', [
    (tuple(), 1, True, 0 ),
    (set(), 1, True, 0 ),
    (list(), 1, True, 0 ),
    (dict(), 1, True, 0 ),
    (my_iterable(0), 0, True, 0 ),
    (my_iterable(0), 1, True, 0 ),
    (my_generator(0), 0, True, 0 ),
    (my_generator(0), 1, True, 0 ),    
    (range(0), 1, True, 0 ),
    ([ 1, 2, 3 ], 1, True, 3 ),
    (my_iterable(3), 0, False, 0 ),
    (my_iterable(3), 1, False, 1 ),
    (my_iterable(3), 5, True, 3 ),
    (my_generator(3), 0, False, 0 ),
    (my_generator(3), 1, False, 1 ),
    (my_generator(3), 5, True, 3 ),    
    (range(3), 0, True, 3 ),
    (range(3), 1, True, 3 ),
    (range(3), 5, True, 3 ),
    ("string", 1, True, 6),
])
def test__len(x: Any, max_try: int, expected_bool: bool, expected_length: int):
    assert _len(x, max_try=max_try) == (expected_bool, expected_length)

@pytest.mark.parametrize('x', [
    len,
    4,
    3.14,
    None
])
def test__len_fails(x: Any):
    with pytest.raises(TypeError):
        _len(x, 1)