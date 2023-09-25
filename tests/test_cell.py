import pytest

from logic.cell import Cell, IceCell, FireCell, DeadCell


def test_create_dead_cell_from_str():
    res = Cell.from_string(' ')
    assert res.__eq__(DeadCell())


def test_create_ice_cell_from_str():
    res = Cell.from_string('I')
    assert res.__eq__(IceCell())


# Negative test
def test_create_cell_error():
    with pytest.raises(ValueError):
        res = Cell.from_string('-')
