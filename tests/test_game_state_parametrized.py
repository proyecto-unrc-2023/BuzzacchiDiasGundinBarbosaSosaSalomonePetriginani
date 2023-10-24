from logic.game_state import GameState, Team
from logic.cell import FireCell, IceCell, Level
from logic.spawn import IceSpawn
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



fight_in_position_params = [
    # Params: board_size, cells_to_add, fight_pos, expected
    ((3, 3), [IceCell(level=Level.LEVEL_1, life=18, position=(0,0)),
              FireCell(level=Level.LEVEL_2, life=30, position=(0,0))], 'F| | \n'\
                                                                       ' | | \n'\
                                                                       ' | | '),
    ((3, 3), [IceCell(level=Level.LEVEL_1, life=18, position=(0,0)), 
              IceCell(level=Level.LEVEL_1, life=18, position=(0,0)), 
              FireCell(level=Level.LEVEL_2, life=30, position=(0,0))], 'F| | \n'\
                                                                       ' | | \n'\
                                                                       ' | | '),
    ((3, 3), [IceCell(level=Level.LEVEL_3, life=50, position=(0,0)), 
              FireCell(level=Level.LEVEL_2, life=35, position=(0,0)), 
              FireCell(level=Level.LEVEL_1, life=10, position=(0,0))], 'I| | \n'\
                                                                       ' | | \n'\
                                                                       ' | | '),
    ((3, 3), [IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              FireCell(level=Level.LEVEL_3, life=42, position=(0,0)), 
              FireCell(level=Level.LEVEL_2, life=25, position=(0,0))], 'I| | \n'\
                                                                       ' | | \n'\
                                                                       ' | | '),
    ((3, 3), [IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              FireCell(level=Level.LEVEL_3, life=43, position=(0,0)), 
              FireCell(level=Level.LEVEL_2, life=25, position=(0,0)), 
              FireCell(level=Level.LEVEL_1, life=20, position=(0,0))], 'I| | \n'\
                                                                       ' | | \n'\
                                                                       ' | | '),
    ((3, 3), [IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              IceCell(level=Level.LEVEL_1, life=20, position=(0,0)), 
              FireCell(level=Level.LEVEL_3, life=43, position=(0,0)), 
              FireCell(level=Level.LEVEL_2, life=25, position=(0,0)), 
              FireCell(level=Level.LEVEL_1, life=20, position=(0,0))], 'I,I| | \n'\
                                                                       ' | | \n'\
                                                                       ' | | '),
    ((3, 3), [IceCell(level=Level.LEVEL_2, life=36, position=(0,0)), 
              IceCell(level=Level.LEVEL_2, life=40, position=(0,0)), 
              IceCell(level=Level.LEVEL_1, life=20, position=(0,0)), 
              FireCell(level=Level.LEVEL_3, life=43, position=(0,0)), 
              FireCell(level=Level.LEVEL_2, life=22, position=(0,0)), 
              FireCell(level=Level.LEVEL_1, life=20, position=(0,0))], 'F,F,F| | \n'\
                                                                       ' | | \n'\
                                                                       ' | | '),
        
]

@pytest.mark.parametrize("board_size, cells_to_add, expected", fight_in_position_params)
def test_execute_fight_in_position(board_size, cells_to_add, expected):
    game_state = GameState()
    game_state.new_game(*board_size)
    for cell in cells_to_add:
        cell.board = game_state.get_board()
        game_state.add_cell(0,0, cell)
    game_state.execute_fight_in_position(0,0)
    assert game_state.get_board().__str__() == expected


execute_fight_in_position_with_spawn_params = [
    ((3, 3), [FireCell(level=Level.LEVEL_2, life=36, position=(0,0))], 264),
    ((3,3), [FireCell(level=Level.LEVEL_3, life=58, position=(0,0)),
             FireCell(level=Level.LEVEL_2, life=36, position=(0,0)),
             FireCell(level=Level.LEVEL_1, life=18, position=(0,0))], 188),
    ((3,3), [FireCell(level=Level.LEVEL_3, life=60, position=(0,0)),
             FireCell(level=Level.LEVEL_3, life=60, position=(0,0)),
             FireCell(level=Level.LEVEL_3, life=60, position=(0,0)),
             FireCell(level=Level.LEVEL_3, life=60, position=(0,0)),
             FireCell(level=Level.LEVEL_3, life=60, position=(0,0)),
             FireCell(level=Level.LEVEL_3, life=60, position=(0,0))], 0)
]

@pytest.mark.parametrize("board_size, cells_to_add, expected_life", execute_fight_in_position_with_spawn_params)
def test_execute_fight_in_position_with_spawn(board_size, cells_to_add, expected_life):

    game_state = GameState()
    game_state.new_game(*board_size)
    game_state.create_spawn(1,1, Team.IceTeam)
    for cell in cells_to_add:
        cell.board = game_state.get_board()
        game_state.add_cell(0,0,cell)
    game_state.execute_fight_in_position(0,0)

    assert game_state.ice_spawn.get_life() == expected_life                                                     
                                                                              