import pytest

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
    board = Board(*board_size)
    for cell in cells_to_add:
        board.add_cell(*cell)
    assert board.__str__() == expected


######Tests para execute_fight_in_position
fight_in_position_params = [
    # Params: board_size, cells_to_add, fight_pos, expected
    ((3, 3), [IceCell(level=Level.LEVEL_1, life=18, position=(0,0)),
              FireCell(level=Level.LEVEL_2, life=30, position=(0,0))], (0, 0), 'F| | \n'\
                                                                               ' | | \n'\
                                                                               ' | | '),
    ((3, 3), [IceCell(level=Level.LEVEL_1, life=18, position=(0,0)), 
              IceCell(level=Level.LEVEL_1, life=18, position=(0,0)), 
              FireCell(level=Level.LEVEL_2, life=30, position=(0,0))], (0, 0), 'F| | \n'\
                                                                               ' | | \n'\
                                                                               ' | | '),
    ((3, 3), [IceCell(level=Level.LEVEL_3, life=50, position=(0,0)), 
              FireCell(level=Level.LEVEL_2, life=35, position=(0,0)), 
              FireCell(level=Level.LEVEL_1, life=10, position=(0,0))], (0, 0), 'I| | \n'\
                                                                               ' | | \n'\
                                                                               ' | | '),
    ((3, 3), [IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              FireCell(level=Level.LEVEL_3, life=42, position=(0,0)), 
              FireCell(level=Level.LEVEL_2, life=25, position=(0,0))], (0, 0), 'I| | \n'\
                                                                               ' | | \n'\
                                                                               ' | | '),
    ((3, 3), [IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              FireCell(level=Level.LEVEL_3, life=43, position=(0,0)), 
              FireCell(level=Level.LEVEL_2, life=25, position=(0,0)), 
              FireCell(level=Level.LEVEL_1, life=20, position=(0,0))], (0, 0), 'I| | \n'\
                                                                               ' | | \n'\
                                                                               ' | | '),
    ((3, 3), [IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              IceCell(level=Level.LEVEL_1, life=20, position=(0,0)), 
              FireCell(level=Level.LEVEL_3, life=43, position=(0,0)), 
              FireCell(level=Level.LEVEL_2, life=25, position=(0,0)), 
              FireCell(level=Level.LEVEL_1, life=20, position=(0,0))], (0, 0), 'I,I| | \n'\
                                                                                ' | | \n'\
                                                                                ' | | '),
    ((3, 3), [IceCell(level=Level.LEVEL_2, life=36, position=(0,0)), 
              IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              IceCell(level=Level.LEVEL_1, life=20, position=(0,0)), 
              FireCell(level=Level.LEVEL_3, life=43, position=(0,0)), 
              FireCell(level=Level.LEVEL_2, life=22, position=(0,0)), 
              FireCell(level=Level.LEVEL_1, life=20, position=(0,0))], (0, 0), 'F,F,F| | \n'\
                                                                               ' | | \n'\
                                                                               ' | | ')
]

@pytest.mark.parametrize("board_size, cells_to_add, fight_pos, expected", fight_in_position_params)
def test_execute_fight_in_position(board_size, cells_to_add, fight_pos, expected):
    board = Board(*board_size)
    for cell in cells_to_add:
        cell.board = board
        board.add_cell_by_tuple(fight_pos, cell)
    board.execute_fight_in_position(*fight_pos)
    assert board.__str__() == expected



############Test para fusion 
fusion_params = [
    # Parameters: initial board size, list of cells to add, expected number of cells, expected types, expected life points, expected levels
    ((10, 10), [(FireCell(level=Level.LEVEL_2, life=36, position=(1, 1))),
                (FireCell(level=Level.LEVEL_1, life=16, position=(1, 1))),
                (FireCell(level=Level.LEVEL_1, life=7, position=(1, 1))),
                (IceCell(level=Level.LEVEL_1, life=2, position=(1, 1))),
                (IceCell(level=Level.LEVEL_1, life=12, position=(1, 1)))], 2, [FireCell, IceCell], [60, 40], [Level.LEVEL_3, Level.LEVEL_2]),
    ((10, 10), [(FireCell(level=Level.LEVEL_1, life=20, position=(1, 1))),
                (FireCell(level=Level.LEVEL_1, life=20, position=(1, 1))),
                (FireCell(level=Level.LEVEL_2, life=40, position=(1, 1))),
                (FireCell(level=Level.LEVEL_2, life=40, position=(1, 1)))], 2, [FireCell,FireCell] ,[60, 40], [Level.LEVEL_3, Level.LEVEL_2]),
    ((10, 10), [(FireCell(level=Level.LEVEL_1, life=20, position=(1, 1))),
                (FireCell(level=Level.LEVEL_1, life=20, position=(1, 1))),
                (FireCell(level=Level.LEVEL_2, life=40, position=(1, 1))),
                (FireCell(level=Level.LEVEL_2, life=40, position=(1, 1))),
                (IceCell(level=Level.LEVEL_2, life=40, position=(1, 1))),
                (IceCell(level=Level.LEVEL_1, life=20, position=(1, 1)))], 4, [FireCell, FireCell, IceCell, IceCell] ,[60,40,40,20], [Level.LEVEL_3, Level.LEVEL_2, Level.LEVEL_2, Level.LEVEL_1])
]

@pytest.mark.parametrize("board_size, cells_to_add, expected_num_cells, expected_types, expected_life_points, expected_levels", fusion_params)
def test_fusion_board(board_size, cells_to_add, expected_num_cells, expected_types, expected_life_points, expected_levels):
    board = Board(*board_size)
    pos = (1, 1)
    for cell in cells_to_add:
        cell.position = pos
        cell.board = board
        board.add_cell(*pos, cell)
    board.fusion(pos)
    cells_in_pos = board.get_cells(*pos)
    assert len(cells_in_pos) == expected_num_cells
    for i in range(expected_num_cells):
        assert isinstance(cells_in_pos[i], expected_types[i])
        assert cells_in_pos[i].life == expected_life_points[i]
        assert cells_in_pos[i].level == expected_levels[i]