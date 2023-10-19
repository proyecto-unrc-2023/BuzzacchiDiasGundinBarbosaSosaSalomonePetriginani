import pytest

from logic.game_state import GameState, Team
from logic.board import Level

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
