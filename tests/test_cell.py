import pytest

from logic.cell import Cell, IceCell, FireCell, DeadCell, Level
from logic.board import Board

@pytest.fixture
def board():
    return Board(rows=3, columns=3)

@pytest.fixture
def cell(board):
    return FireCell(board=board)

@pytest.fixture
def fire_cell(board):
    return FireCell(board=board, level=Level.LEVEL_1, life=12, position=(1,1))

@pytest.fixture
def ice_cell(board):
    return IceCell(board=board, level=Level.LEVEL_1, life=2, position=(1,1))

@pytest.fixture
def ice_cell2(board):
    return IceCell(board=board, level=Level.LEVEL_1, life=5, position=(2,2))

@pytest.fixture
def ice_cell3(board):
    return IceCell(board=board, level=Level.LEVEL_1, life=10, position=(2,2))

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


###########   Tests for fight   ###########
def test_fight_same_position_different_types(board, fire_cell, ice_cell):
    # Asegúrate de que las celdas estén en la misma posición
    fire_cell.position = ice_cell.position = (1, 1)
    
    #fire_cell.set_life(5)
    board.board[1][1].append(fire_cell)
    board.board[1][1].append(ice_cell)
    
    fire_cell.fight(ice_cell)
    
    assert fire_cell in board.get_cells(1,1)
    assert ice_cell not in board.get_cells(1,1)

def test_fight_same_position_same_type_higher_level(board, fire_cell):
    higher_level_ice_cell = IceCell(board=board, level=Level.LEVEL_2, life=21, position=(1,1))
    
    board.board[1][1].append(fire_cell)
    board.board[1][1].append(higher_level_ice_cell)
    
    fire_cell.fight(higher_level_ice_cell)

    assert fire_cell not in board.board[1][1]
    assert higher_level_ice_cell in board.board[1][1]

def test_fight_same_position_same_type_same_level_higher_life(board, ice_cell):
    higher_life_fire_cell = FireCell(board=board, level=Level.LEVEL_1, life=8, position=(1,1))
    
    board.board[1][1].append(ice_cell)
    board.board[1][1].append(higher_life_fire_cell)
    
    ice_cell.fight(higher_life_fire_cell)
    
    assert ice_cell not in board.board[1][1]
    assert higher_life_fire_cell in board.board[1][1]

def test_fight_same_position_same_type_same_level_same_life(board, fire_cell, ice_cell):    
    board.board[1][1].append(fire_cell)
    board.board[1][1].append(ice_cell)
    
    fire_cell.set_life(ice_cell.get_life())
    fire_cell.fight(ice_cell)
    
    cells_expected = board.get_cells(fire_cell.position[0], fire_cell.position[1])
    assert len(cells_expected) == 1
    assert isinstance(cells_expected[0], DeadCell)

def test_fight_same_position_different_types_low_life(board, fire_cell, ice_cell):
    fire_cell.position = ice_cell.position = (1, 1)
    fire_cell.set_life(3)
    ice_cell.set_life(3)
    board.board[1][1].append(fire_cell)
    board.board[1][1].append(ice_cell)
    
    fire_cell.fight(ice_cell)
    
    assert fire_cell not in board.get_cells(1,1)
    assert ice_cell not in board.get_cells(1,1)

def test_fight_same_position_different_types_lower_level_high_life(board):
    lower_level_fire_cell = FireCell(board=board, level=Level.LEVEL_2, life=25, position=(1, 1))
    higher_level_ice_cell = IceCell(board=board, level=Level.LEVEL_3, life=41, position=(1, 1))

    board.board[1][1].append(lower_level_fire_cell)
    board.board[1][1].append(higher_level_ice_cell)

    lower_level_fire_cell.fight(higher_level_ice_cell)

    assert lower_level_fire_cell not in board.get_cells(1, 1)
    assert higher_level_ice_cell in board.get_cells(1, 1)
    
def test_fusion_two_level_1_ice_cells(board, ice_cell2, ice_cell3):
    board.board[2][2].append(ice_cell2)
    board.board[2][2].append(ice_cell3)
    
    ice_cell2.fusion(ice_cell3)
    
    cells_expected = board.get_cells(ice_cell2.position[0], ice_cell2.position[1])
    assert ice_cell2.level == Level.LEVEL_2
    assert ice_cell2.life == 40
    assert len(cells_expected) == 1
    assert isinstance(cells_expected[0], IceCell)

def test_fight_same_position_different_types_low_life(board, fire_cell, ice_cell):
    fire_cell.position = ice_cell.position = (1, 1)
    fire_cell.set_life(3)
    ice_cell.set_life(3)
    board.board[1][1].append(fire_cell)
    board.board[1][1].append(ice_cell)
    
    fire_cell.fight(ice_cell)
    
    assert fire_cell not in board.get_cells(1,1)
    assert ice_cell not in board.get_cells(1,1)

def test_fight_same_position_different_types_lower_level_high_life(board):
    lower_level_fire_cell = FireCell(board=board, level=Level.LEVEL_2, life=25, position=(1, 1))
    higher_level_ice_cell = IceCell(board=board, level=Level.LEVEL_3, life=41, position=(1, 1))

    board.board[1][1].append(lower_level_fire_cell)
    board.board[1][1].append(higher_level_ice_cell)

    lower_level_fire_cell.fight(higher_level_ice_cell)

    assert lower_level_fire_cell not in board.get_cells(1, 1)
    assert higher_level_ice_cell in board.get_cells(1, 1)