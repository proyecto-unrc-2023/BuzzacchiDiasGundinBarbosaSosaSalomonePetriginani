import pytest
import random
from logic.board import Board
from logic.cell import FireCell, IceCell, Cell, DeadCell, Level

empty_board_params = [
    (2,2, ' | \n'\
          ' | '),
    (2,3, ' | | \n'\
          ' | | '),
    (4,4, ' | | | \n'\
          ' | | | \n'\
          ' | | | \n'\
          ' | | | '),
    (2,4, ' | | | \n'\
          ' | | | '),
    (6,5, ' | | | | \n'\
          ' | | | | \n'\
          ' | | | | \n'\
          ' | | | | \n'\
          ' | | | | \n'\
          ' | | | | '),
    (50,50, (' |' * 49 + ' \n') * 49 + ' |' * 49 + ' ')
]

@pytest.mark.parametrize("rows, columns, expected", empty_board_params)
def test_empty_board_to_string(rows, columns, expected):
    board = Board(rows, columns)
    res = board.__str__()
    assert expected == res



board_with_cells_params = [
    # Parameters: initial board size, list of cells to add, expected board configuration
    ((2, 2), [(0, 0, IceCell()), (0, 0, FireCell())], 'F,I| \n'\
                                                      ' | '),
    ((2, 2), [(0, 0, IceCell()), (0, 0, FireCell()), (1, 1, FireCell()), (1, 1, FireCell())], 'F,I| \n'\
                                                                                              ' |F,F'),
    ((3, 3), [(0, 0, IceCell()), (0, 0, FireCell()), (2, 2, FireCell()), (1, 2, IceCell())], 'F,I| | \n'\
                                                                                             ' | |I\n'\
                                                                                             ' | |F'),
    ((4, 3), [(0, 0, FireCell()), (2, 2, IceCell()), (1, 1, FireCell()), (3, 0, FireCell())], 'F| | \n'\
                                                                                              ' |F| \n'\
                                                                                              ' | |I\n'\
                                                                                              'F| | '),
    ((3, 3), [(1, 1, IceCell()), (1, 1, FireCell()), (2, 2, FireCell()), (0, 2, IceCell())], ' | |I\n'\
                                                                                             ' |F,I| \n'\
                                                                                             ' | |F'),
    ((4, 4), [(3, 3, FireCell()), (2, 2, IceCell()), (1, 1, FireCell()), (0, 0, FireCell())], 'F| | | \n'\
                                                                                              ' |F| | \n'\
                                                                                              ' | |I| \n'\
                                                                                              ' | | |F')
]

@pytest.mark.parametrize("board_size, cells_to_add, expected", board_with_cells_params)
def test_board_with_cells(board_size, cells_to_add, expected):
    board = Board(*board_size)
    for cell in cells_to_add:
        board.add_cell(*cell)
    assert board.__str__() == expected