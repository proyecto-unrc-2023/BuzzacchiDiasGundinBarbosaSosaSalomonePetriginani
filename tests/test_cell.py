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
def fire_cell():
    return FireCell(level=Level.LEVEL_1, life=12, position=(1,1))

@pytest.fixture
def ice_cell():
    return IceCell(level=Level.LEVEL_1, life=6, position=(1,1))

@pytest.fixture
def ice_cell2():
    return IceCell(level=Level.LEVEL_1, life=5, position=(2,2))

@pytest.fixture
def ice_cell3():
    return IceCell(level=Level.LEVEL_1, life=10, position=(2,2))

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

###########   Tests for fight   ###########
def test_fight_same_position_different_types(board, fire_cell, ice_cell):
    # Asegúrate de que las celdas estén en la misma posición
    fire_cell.position = ice_cell.position = (1, 1)
    
    board.add_cell(*fire_cell.get_position(), fire_cell)
    board.add_cell(*ice_cell.get_position(), ice_cell)
    
    fire_cell.fight(ice_cell)
    
    assert fire_cell.get_life() == 8
    assert ice_cell.get_life() == 0

def test_fight_same_position_same_type_higher_level(board, fire_cell):
    higher_level_ice_cell = IceCell(level=Level.LEVEL_2, life=21, position=(1,1))
    
    board.add_cell(*fire_cell.get_position(),fire_cell)
    board.add_cell(*higher_level_ice_cell.get_position(), higher_level_ice_cell)
    
    fire_cell.fight(higher_level_ice_cell)

    assert fire_cell.get_life() == 0
    assert higher_level_ice_cell.get_life() == 17

def test_fight_same_position_same_type_same_level_higher_life(board, ice_cell):
    higher_life_fire_cell = FireCell(level=Level.LEVEL_1, life=8, position=(1,1))
    
    board.add_cell(*ice_cell.get_position(), ice_cell)
    board.add_cell(*higher_life_fire_cell.get_position(), higher_life_fire_cell)
    
    ice_cell.fight(higher_life_fire_cell)
    
    assert ice_cell.get_life() == 0
    assert higher_life_fire_cell.get_life() == 4

def test_fight_same_position_same_type_same_level_same_life(board, fire_cell, ice_cell):    
    fire_cell.set_life(ice_cell.get_life())
    
    board.add_cell(*fire_cell.get_position(), fire_cell)
    board.add_cell(*ice_cell.get_position(), ice_cell)
    
    fire_cell.fight(ice_cell)
    
    assert fire_cell.get_life() == 0
    assert ice_cell.get_life() == 0

def test_fight_same_position_different_types_low_life(board, fire_cell, ice_cell):
    fire_cell.set_life(3)
    ice_cell.set_life(3)
    
    board.add_cell(*fire_cell.get_position(), fire_cell)
    board.add_cell(*ice_cell.get_position(), ice_cell)
    
    fire_cell.fight(ice_cell)
    
    assert fire_cell.get_life() == 0
    assert ice_cell.get_life() == 0

def test_fight_same_position_different_types_lower_level_high_life(board):
    lower_level_fire_cell = FireCell(level=Level.LEVEL_2, life=25, position=(1, 1))
    higher_level_ice_cell = IceCell(level=Level.LEVEL_3, life=41, position=(1, 1))

    board.add_cell(*lower_level_fire_cell.get_position(), lower_level_fire_cell)
    board.add_cell(*higher_level_ice_cell.get_position(), higher_level_ice_cell)

    lower_level_fire_cell.fight(higher_level_ice_cell)

    assert lower_level_fire_cell.get_life() == 0
    assert higher_level_ice_cell.get_life() == 37
    
