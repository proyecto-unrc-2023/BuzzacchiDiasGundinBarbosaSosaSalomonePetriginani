from logic.board import Board
from logic.cell import IceCell, FireCell, DeadCell, Level, Cell
from logic.healing_area import HealingArea
import pytest

@pytest.fixture
def healing_area_positions():
    return [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

healing_area_params = [
    # Parameters: initial board size, cell to be healed, expected life, expected level
    ((10, 10), IceCell(board=Board(10, 10), level=Level.LEVEL_1, life=15, position=(1,1)), 18, Level.LEVEL_1),
    ((10, 10), IceCell(board=Board(10, 10), level=Level.LEVEL_1, life=19, position=(1,1)), 22, Level.LEVEL_2),
    ((10, 10), IceCell(board=Board(10, 10), level=Level.LEVEL_3, life=60, position=(1,1)), 60, Level.LEVEL_3),
    ((10, 10), IceCell(board=Board(10, 10), level=Level.LEVEL_1, life=18, position=(1,1)), 21, Level.LEVEL_2)

]

@pytest.mark.parametrize("board_size, cell_to_be_healed, expected_life, expected_level", healing_area_params)
def test_healing_area(board_size, cell_to_be_healed, expected_life, expected_level, healing_area_positions):
    board = Board(*board_size)
    healing_area_positions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
    ice_healing_area = HealingArea(board=board, positions=healing_area_positions,
                                   duration=20,
                                   affected_cell_type=IceCell)
    board.add_cell_by_tuple(cell_to_be_healed.position,
                            cell_to_be_healed)
    ice_healing_area.apply_effect()
    assert board.get_cells(*cell_to_be_healed.position)[0].get_life() == expected_life
    assert board.get_cells(*cell_to_be_healed.position)[0].get_level() == expected_level

#Negative test
def test_firecell_not_healed_by_ice_healing_area(healing_area_positions):
    board_size = (10, 10)
    board = Board(*board_size)
    ice_healing_area = HealingArea(board=board, positions=healing_area_positions,
                                   duration=20,
                                   affected_cell_type=IceCell)
    fire_cell = FireCell(board=board, level=Level.LEVEL_1, life=15, position=(1,1))
    board.add_cell_by_tuple(fire_cell.position,
                            fire_cell)
    ice_healing_area.apply_effect()
    assert board.get_cells(*fire_cell.position)[0].get_life() == 15
    assert board.get_cells(*fire_cell.position)[0].get_level() == Level.LEVEL_1
