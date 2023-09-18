import pytest

from logic.spawn import Spawn, IceSpawn, FireSpawn

def test_create_ice_spawn_from_str():
    res = Spawn.from_string("IS")
    assert res.__eq__(IceSpawn())
    
def test_create_fire_spawn_from_str():
    res = Spawn.from_string("FS")
    assert res.__eq__(FireSpawn())
    
#Negative test
def test_create_spawn_error():
    with pytest.raises(ValueError):
        res = Spawn.from_string('-')