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
    board.create_spawn(1,1, IceSpawn)
    spawn = board.get_box(1,1).get_spawn()
    adjacents_spawn = spawn.get_adjacents_spawn(board.__len__())
    list = [(3, 3), (3, 2), (3, 1), (3, 0), (2, 3), (1, 3), (0, 3)]
    assert set(adjacents_spawn) == set(list)

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

    