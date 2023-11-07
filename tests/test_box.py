from logic.box import Box
from logic.cell import IceCell, FireCell, Level
from logic.spawn import IceSpawn, FireSpawn
from logic.healing_area import HealingArea
import pytest


def test_str_box():
    box = Box()
    box.add_fire_cell(FireCell())
    box.set_spawn(IceSpawn())
    assert str(box) == 'IS,F'

def test_str_box_by_stats():
    box = Box()
    fire_cell_1 = FireCell(level=Level.LEVEL_3, life=54)
    fire_cell_2 = FireCell()
    fire_cell_3 = FireCell(level=Level.LEVEL_3, life = 60)
    box.add_fire_cell(fire_cell_1 )
    box.add_fire_cell(fire_cell_2 )
    box.add_fire_cell(fire_cell_3 )
    assert box.get_fire_cells()[0] is fire_cell_3

def test_box_equality():
    # Crear instancias de los objetos necesarios para los Box
    spawn1 = IceSpawn(positions=[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])  
    fire_cells1 = [FireCell(), FireCell()]  
    ice_cells1 = [IceCell(), IceCell()]  
    fire_healing_area1 = HealingArea(positions=[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)], affected_cell_type=FireCell)  
    ice_healing_area1 = None  
    pos1 = (0, 0)

    spawn2 = IceSpawn(positions=[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])  
    ice_cells2 = [IceCell(), IceCell()]
    fire_cells2 = [FireCell(), FireCell()]  
    fire_healing_area2 = HealingArea(positions=[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)], affected_cell_type=FireCell)
    ice_healing_area2 = None
    pos2 = (0, 0)

    # Crear dos Box con estados idénticos
    box1 = Box(spawn1, fire_cells1, ice_cells1, fire_healing_area1, ice_healing_area1, pos1)
    box2 = Box(spawn2, fire_cells2, ice_cells2, fire_healing_area2, ice_healing_area2, pos2)

    # Assert para verificar que box1 y box2 son iguales
    assert box1 == box2, "Las instancias de Box deberían ser iguales"
