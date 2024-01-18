from logic.board import Board
from logic.cell import IceCell, FireCell, DeadCell, Level, Cell
from logic.healing_area import HealingArea
import pytest

@pytest.fixture
def healing_area_positions():
    return [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

healing_area_params = [
    # Parameters: initial board size, cell to be healed, expected life, expected level
    ((10, 10), [IceCell(level=Level.LEVEL_1, life=15, position=(1,1))], 18, Level.LEVEL_1),
    ((10, 10), [IceCell(level=Level.LEVEL_1, life=19, position=(1,1))], 22, Level.LEVEL_2),
    ((10, 10), [IceCell(level=Level.LEVEL_4, life=80, position=(1,1))], 80, Level.LEVEL_4),
    ((10, 10), [IceCell(level=Level.LEVEL_1, life=18, position=(1,1))], 21, Level.LEVEL_2)

]

@pytest.mark.parametrize("board_size, cell_to_be_healed, expected_life, expected_level", healing_area_params)
def test_healing_area(board_size, cell_to_be_healed, expected_life, expected_level, healing_area_positions):
    board = Board(*board_size)
    ice_healing_area = HealingArea(positions=healing_area_positions, affected_cell_type=IceCell)
    duration = ice_healing_area.duration
    board.add_cell(*cell_to_be_healed[0].position, cell_to_be_healed[0])
    board.add_healing_area((1,1),ice_healing_area)
    ice_healing_area.apply_effect(cell_to_be_healed)
    assert board.get_cells(*cell_to_be_healed[0].position)[0].get_life() == expected_life
    assert board.get_cells(*cell_to_be_healed[0].position)[0].get_level() == expected_level
    #assert duration - 1 == ice_healing_area.duration


def test_opposing_team_cell_damaged_in_healing_area(healing_area_positions):
    board_size = (10, 10)
    board = Board(*board_size)

    opposing_team_cell = [FireCell(level=Level.LEVEL_1, life=15, position=(1, 2))]  # Por ejemplo, posición diferente al área de curación
    board.add_cell(*opposing_team_cell[0].position, opposing_team_cell[0])

    ice_healing_area = HealingArea(positions=healing_area_positions, affected_cell_type=IceCell)
    board.add_healing_area((1, 1), ice_healing_area)

    ice_healing_area.apply_effect(opposing_team_cell)

    assert board.get_cells(*opposing_team_cell[0].position)[0].get_life() < 15
