import pytest
from ...t22 import adv_2022_22 as unit_test

@pytest.mark.parametrize("test_input,expected", [("N", [-1,0]), ("S", [1,0])])
def test_simple(test_input, expected):
    dir = unit_test.getDirection(test_input)
    assert dir == expected
