import pytest
from aoc2022.src.aoc.t22 import adv_2022_22 as unit_test

@pytest.mark.parametrize("test_input,expected", [("N", [-1,0]), ("S", [1,0])])
def test_get_direction(test_input, expected):
    dir = unit_test.get_direction(test_input)
    assert dir == expected

@pytest.mark.parametrize("test_input,expected", [("N", "W"), ("W", "S"), ("S", "E"), ("E", "N")])
def test_get_next_left_dir(test_input, expected):
    dir = unit_test.get_next_left_dir(test_input)
    assert dir == expected

@pytest.mark.parametrize("test_input,expected", [("N", "E"), ("E", "S"),("S", "W"),("W", "N")])
def test_get_next_right_dir(test_input, expected):
    dir = unit_test.get_next_right_dir(test_input)
    assert dir == expected

