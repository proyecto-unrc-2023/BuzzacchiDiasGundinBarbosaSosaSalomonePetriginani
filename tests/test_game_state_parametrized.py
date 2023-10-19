from logic.game_state import GameState, Team
import pytest

params = [
    ((50, 50), (24,24), Team.IceTeam, [(23, 23), (23, 24), (23, 25), (24, 23), (24, 24), (24, 25), (25, 23), (25, 24), (25, 25)]),
    ((50, 50), (1,1), Team.IceTeam, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]),
    ((50, 50), (48,48), Team.FireTeam, [(47, 47), (47, 48), (47, 49), (48, 47), (48, 48), (48, 49), (49, 47), (49, 48), (49, 49)]),
]

@pytest.mark.parametrize("board_size, spawn_pos, team_type, expected_positions", params)
def test_create_spawn(board_size, spawn_pos, team_type, expected_positions):
    game_state = GameState()
    game_state.new_game(*board_size)
    game_state.set_team(team_type)
    game_state.create_spawn(*spawn_pos, team_type)
    if team_type == Team.IceTeam:
        assert game_state.ice_spawn is not None
        assert set(game_state.ice_spawn.positions) == set(expected_positions)
    else:
        assert game_state.fire_spawn is not None
        assert set(game_state.fire_spawn.positions) == set(expected_positions)

edge_params = [
    ((50, 50), (0,0), Team.IceTeam),
    ((50, 50), (0,49), Team.FireTeam),
    ((50, 50), (49,0), Team.IceTeam),
    ((50, 50), (49,49), Team.FireTeam),
]

@pytest.mark.parametrize("board_size, spawn_pos, team_type", edge_params)
def test_create_spawn_on_edge(board_size, spawn_pos, team_type):
    game_state = GameState()
    game_state.new_game(*board_size)
    game_state.set_team(team_type)
    with pytest.raises(ValueError):
        game_state.create_spawn(*spawn_pos, team_type.value)
