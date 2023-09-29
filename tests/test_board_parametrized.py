import pytest

from logic.board import Board
from logic.cell import FireCell, IceCell, Cell, DeadCell

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
    ((2, 2), [(0, 0, IceCell()), (0, 0, FireCell())], 'I,F| \n'\
                                                      ' | '),
    ((2, 2), [(0, 0, IceCell()), (0, 0, FireCell()), (1, 1, FireCell()), (1, 1, FireCell())], 'I,F| \n'\
                                                                                              ' |F,F'),
    ((3, 3), [(0, 0, IceCell()), (0, 0, FireCell()), (2, 2, FireCell()), (1, 2, IceCell())], 'I,F| | \n'\
                                                                                             ' | |I\n'\
                                                                                             ' | |F'),
    ((4, 3), [(0, 0, FireCell()), (2, 2, IceCell()), (1, 1, FireCell()), (3, 0, FireCell())], 'F| | \n'\
                                                                                              ' |F| \n'\
                                                                                              ' | |I\n'\
                                                                                              'F| | ')
]

@pytest.mark.parametrize("board_size, cells_to_add, expected", board_with_cells_params)
def test_board_with_cells(board_size, cells_to_add, expected):
    # Create a board with the specified size
    board = Board(*board_size)

    # Add each cell to the board
    for cell in cells_to_add:
        board.add_cell(*cell)

    # Verify that the board has the expected configuration
    assert board.__str__() == expected
'''
def test_board_with_ice_and_fire_cells():
    # Crea un tablero 2x2
    board = Board(2, 2)

    # Agrega una célula de hielo en la posición (0,0)
    board.add_cell(0, 0, IceCell())

    # Agrega una célula de fuego en la posición (0,0)
    board.add_cell(0, 0, FireCell())

    # Verifica que el tablero tenga la configuración esperada
    expected_board_str = 'I,F| \n'\
                         ' | '
    assert board.__str__() == expected_board_str

def test2_board_with_ice_and_fire_cells():
    # Crea un tablero 2x2
    board = Board(2, 2)

    # Agrega una célula de hielo en la posición (0,0)
    board.add_cell(0, 0, IceCell())

    # Agrega una célula de fuego en la posición (0,0)
    board.add_cell(0, 0, FireCell())

    board.add_cell(1, 1, FireCell())
    board.add_cell(1, 1, FireCell())

    # Verifica que el tablero tenga la configuración esperada
    expected_board_str = 'I,F| \n'\
                         ' |F,F'
    assert board.__str__() == expected_board_str
'''
