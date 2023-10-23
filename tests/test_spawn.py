import pytest
from logic.spawn import Spawn, IceSpawn, FireSpawn
from logic.board import Board

def test_create_ice_spawn_from_str():
    res = Spawn.from_string("IS")
    assert res.__eq__(IceSpawn())
    
def test_create_fire_spawn_from_str():
    res = Spawn.from_string("FS")
    assert res.__eq__(FireSpawn())
    
def test_create_spawn_error():
    with pytest.raises(ValueError):
        res = Spawn.from_string('-')

def test_generate_cells_with_position():
    board = Board(10, 10)
    spawn = FireSpawn(position=(5, 5), board=board)
    spawn.generate_cells()
    cantCells = 0
    for i in range(10):
        for j in range(10):
            if(board.get_cells(i, j).__str__() == 'F'):
                cantCells += 1
    assert 0 <= cantCells <= 4

def test_decrease_life_with_no_damage():
    spawn = FireSpawn(life=10)
    spawn.decrease_life(0)
    assert spawn.life == 10

def test_decrease_life_with_damage():
    spawn = FireSpawn(life=10)
    spawn.decrease_life(5)
    assert spawn.life == 5

def test_decrease_life_with_excessive_damage():
    spawn = FireSpawn(life=10)
    spawn.decrease_life(15)
    assert spawn.life == 0
    
def test_create_spawn_from_valid_str():
    res = Spawn.from_string("SP")
    assert isinstance(res, Spawn)

def test_create_spawn_from_valid_str_with_position():
    board = Board(10, 10)
    res = Spawn.from_string("SP")
    res.set_board(board)
    res.set_position((5, 5))
    assert isinstance(res, Spawn)
    assert res.position == (5, 5)
    assert res.board == board