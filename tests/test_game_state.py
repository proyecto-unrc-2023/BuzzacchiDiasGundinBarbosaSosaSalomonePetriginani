import pytest

from logic.game_state import GameState, Team
from logic.board import Level
from logic.cell import FireCell, IceCell, Cell

@pytest.fixture
def gamestate():
    game_state = GameState()
    game_state.new_game(3, 3)
    return game_state

def test_advance_method(gamestate):
    gamestate.set_team(Team.FireTeam)
    gamestate.create_cell(1, 1, gamestate.get_team(), Level.LEVEL_1, 20)
    oldcell = gamestate.get_cells(1, 1)

    gamestate.move_cells_in_position(1, 1)
    result = gamestate.get_board()

    assert oldcell in [
        result.get_cells(0, 0), result.get_cells(0, 1), result.get_cells(0, 2),
        result.get_cells(1, 0), result.get_cells(1, 2), result.get_cells(2, 0),
        result.get_cells(2, 1), result.get_cells(2, 2)
    ]

## TEST Fusion of Board
def test_fusion_board(gamestate):
    pos = (1,1)
    gamestate.create_cell(pos[0], pos[1], team=Team.FireTeam, level=Level.LEVEL_2, life=36)
    gamestate.create_cell(pos[0], pos[1], team=Team.FireTeam, level=Level.LEVEL_1, life=16)
    gamestate.create_cell(pos[0], pos[1], team=Team.FireTeam, level=Level.LEVEL_1, life=7)
    gamestate.create_cell(pos[0], pos[1], team=Team.IceTeam, level=Level.LEVEL_1, life=2)
    gamestate.create_cell(pos[0], pos[1], team=Team.IceTeam, level=Level.LEVEL_1, life=12)
    gamestate.fusion(pos)
    cells_in_pos = gamestate.get_cells(pos[0], pos[1])
    assert len(cells_in_pos) == 2
    assert isinstance(cells_in_pos[0], FireCell)
    assert isinstance(cells_in_pos[1], IceCell)
    assert cells_in_pos[0].get_life() == 60
    assert cells_in_pos[0].get_level() == Level.LEVEL_3
    assert cells_in_pos[1].get_life() == 40
    assert cells_in_pos[1].get_level() == Level.LEVEL_2
    
def test_fusion_in_all_board(gamestate):
    pos0 = (0,0)
    gamestate.create_cell(pos0[0], pos0[1], Team.IceTeam, level=Level.LEVEL_2, life=36)
    gamestate.create_cell(pos0[0], pos0[1], Team.IceTeam, level=Level.LEVEL_2, life=30,)

    pos1 = (0,1)
    gamestate.create_cell(pos1[0], pos1[1], Team.IceTeam, level=Level.LEVEL_1, life=15)
    gamestate.create_cell(pos1[0], pos1[1], Team.IceTeam, level=Level.LEVEL_1, life=2)

    pos2 = (1,0)
    gamestate.create_cell(pos2[0], pos2[1], Team.FireTeam, level=Level.LEVEL_3, life=48)
    gamestate.create_cell(pos2[0], pos2[1], Team.IceTeam, level=Level.LEVEL_1, life=15)
    
    pos3 = (1,1)
    gamestate.create_cell(pos3[0], pos3[1], Team.FireTeam, level=Level.LEVEL_3, life=50)
    gamestate.create_cell(pos3[0], pos3[1], Team.FireTeam, level=Level.LEVEL_2, life=29)

    gamestate.execute_fusions_in_all_positions()

    cells_in_pos_00 = gamestate.get_cells(0, 0)
    cells_in_pos_01 = gamestate.get_cells(0, 1)
    cells_in_pos_10 = gamestate.get_cells(1, 0)
    cells_in_pos_11 = gamestate.get_cells(1, 1)

    # Comprueba la fusión en (0, 0)
    assert len(cells_in_pos_00) == 1
    assert isinstance(cells_in_pos_00[0], IceCell)
    assert cells_in_pos_00[0].life == 60
    assert cells_in_pos_00[0].level == Level.LEVEL_3

    # Comprueba la fusión en (0, 1)
    assert len(cells_in_pos_01) == 1
    assert isinstance(cells_in_pos_01[0], IceCell)
    assert cells_in_pos_01[0].life == 40
    assert cells_in_pos_01[0].level == Level.LEVEL_2

    # Comprueba la fusión en (1, 0)
    assert len(cells_in_pos_10) == 2
    assert isinstance(cells_in_pos_10[0], FireCell)
    assert isinstance(cells_in_pos_10[1], IceCell)
    assert cells_in_pos_10[0].life == 48
    assert cells_in_pos_10[0].level == Level.LEVEL_3
    assert cells_in_pos_10[1].life == 15
    assert cells_in_pos_10[1].level == Level.LEVEL_1

    # Comprueba que no hubo fusión en (1, 1)
    assert len(cells_in_pos_11) == 2
    assert isinstance(cells_in_pos_11[0], FireCell)
    assert isinstance(cells_in_pos_11[1], FireCell)
    assert cells_in_pos_11[0].life == 50
    assert cells_in_pos_11[0].level == Level.LEVEL_3
    assert cells_in_pos_11[1].life == 29
    assert cells_in_pos_11[1].level == Level.LEVEL_2