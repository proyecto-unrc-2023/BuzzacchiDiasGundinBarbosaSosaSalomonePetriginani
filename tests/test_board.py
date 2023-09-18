import pytest

from logic.board import Board
from logic.cell import IceCell, FireCell, DeadCell, Cell

@pytest.fixture
def board():
    return Board(2, 2)

def test_initial_board(board):
    assert board.rows == 2
    assert board.columns == 2
    assert board.get_cell(0, 0).__eq__(DeadCell())
    assert board.get_cell(0, 1).__eq__(DeadCell())
    assert board.get_cell(1, 0).__eq__(DeadCell())
    assert board.get_cell(1, 1).__eq__(DeadCell())

def test_put_one_fire_cell(board):
    board.put_cell(1, 0, FireCell())
    assert board.get_cell(0, 0).__eq__(DeadCell())
    assert board.get_cell(0, 1).__eq__(DeadCell())
    assert board.get_cell(1, 0).__eq__(FireCell())
    assert board.get_cell(1, 1).__eq__(DeadCell())

def test_put_one_ice_cell(board):
    board.put_cell(1, 0, IceCell())
    assert board.get_cell(0, 0).__eq__(DeadCell())
    assert board.get_cell(0, 1).__eq__(DeadCell())
    assert board.get_cell(1, 0).__eq__(IceCell())
    assert board.get_cell(1, 1).__eq__(DeadCell())

def test_put_fire_cell_fails(board):
    board.put_fire_cell(1, 0)
    with pytest.raises(ValueError):
        board.put_fire_cell(1, 0)

def test_put_ice_cell_fails(board):
    board.put_ice_cell(1, 0)
    with pytest.raises(ValueError):
        board.put_ice_cell(1, 0)

def test_empty_board_to_string(board):
    res = board.__str__()
    expected = ' | \n' \
               ' | '
    assert expected == res

def test_board_with_two_cells_to_string(board):
    board.put_fire_cell(1, 1)
    board.put_ice_cell(0, 0)
    res = board.__str__()
    expected = 'I| \n' \
               ' |F'
    assert expected == res


