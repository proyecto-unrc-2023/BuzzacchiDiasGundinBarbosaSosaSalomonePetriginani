import pytest

from logic.cell import Cell, IceCell, FireCell, DeadCell
from logic.board import Board

@pytest.fixture
def board():
    return Board(rows=3, columns=3)

@pytest.fixture
def cell(board):
    return FireCell(board=board)

@pytest.fixture
def fire_cell(board):
    return FireCell(board=board, level=1, life=2, position=(1,1))

@pytest.fixture
def ice_cell(board):
    return IceCell(board=board, level=1, life=2, position=(1,1))

def test_create_dead_cell_from_str():
    res = Cell.from_string(' ')
    assert isinstance(res, DeadCell)

def test_create_ice_cell_from_str():
    res = Cell.from_string('I')
    assert isinstance(res, IceCell)


# Negative test
def test_create_cell_error():
    with pytest.raises(ValueError):
        res = Cell.from_string('-')


#Test that a cell on an empty board correctly identifies its adjacent cells.
def test_get_adjacents_empty_board(cell, board):
    assert cell.get_adjacents_for_move((0, 0)) == [board.get_cells(0, 1), board.get_cells(1, 0), board.get_cells(1, 1)]


#Test that a cell in the center of the board with neighbors correctly identifies its adjacent cells.
def test_get_adjacents_for_move_center_fire_cell(cell, board):
    board.add_cell(1, 1, FireCell())
    assert cell.get_adjacents_for_move((1, 1)) == [board.get_cells(0, 0), board.get_cells(0, 1), board.get_cells(0, 2),
                                                   board.get_cells(1, 0), board.get_cells(1, 2), board.get_cells(2, 0),
                                                   board.get_cells(2, 1), board.get_cells(2, 2)]


#Test that a cell in a corner of the board with neighbors correctly identifies its adjacent cells.
def test_get_adjacents_for_move_corner_fire_cell(cell, board):
    board.add_cell(0, 0, FireCell())
    assert cell.get_adjacents_for_move((0, 0)) == [board.get_cells(0, 1), board.get_cells(1, 0), board.get_cells(1, 1)]


#Test that a cell on an edge of the board with neighbors correctly identifies its adjacent cells.
def test_get_adjacents_for_move_edge_fire_cell(cell, board):
    board.add_cell(1, 0, FireCell())
    assert cell.get_adjacents_for_move((1, 0)) == [board.get_cells(0, 0), board.get_cells(0, 1), board.get_cells(1, 1), board.get_cells(2, 0), board.get_cells(2, 1)]


def test_advance_method(cell, board):
    example_board = [
        [None, None, None],
        [None, cell, None],
        [None, None, None],
    ]

    board.board = example_board

    result = cell.advance()

    assert result in [
        example_board[0][0], example_board[0][1], example_board[0][2],
        example_board[1][0], example_board[1][2],
        example_board[2][0], example_board[2][1], example_board[2][2]
    ]

