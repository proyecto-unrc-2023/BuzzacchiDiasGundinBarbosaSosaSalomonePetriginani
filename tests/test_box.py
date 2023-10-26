from logic.box import Box
from logic.cell import IceCell, FireCell, Level
from logic.spawn import IceSpawn, FireSpawn
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

