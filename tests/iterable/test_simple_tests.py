import pytest
from assertiterables.iterables import is_iterable, single, empty

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
    (dict(), True)
])
def test_is_iterable(x, outcome):
    assert is_iterable(x) == outcome

