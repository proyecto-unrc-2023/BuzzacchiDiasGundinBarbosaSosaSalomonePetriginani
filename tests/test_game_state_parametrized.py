from logic.game_state import GameState, Team
from logic.cell import FireCell, IceCell, Level
from logic.spawn import IceSpawn, FireSpawn
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
    spawn_type = IceSpawn if team_type == Team.IceTeam else FireSpawn
    game_state.create_spawn(*spawn_pos, spawn_type)
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
        game_state.add_cell(0,0, cell)
    game_state.execute_fight_in_position(0,0)
    assert game_state.get_board().__str__() == expected


execute_fight_in_position_with_spawn_params = [
    ((10,10), [FireCell(level=Level.LEVEL_2, life=36, position=(0,0))], 264),
    ((10,10), [FireCell(level=Level.LEVEL_3, life=58, position=(0,0)),
             FireCell(level=Level.LEVEL_2, life=36, position=(0,0)),
             FireCell(level=Level.LEVEL_1, life=18, position=(0,0))], 188),
    ((10,10), [FireCell(level=Level.LEVEL_3, life=60, position=(0,0)),
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
    game_state.create_spawn(1,1, IceSpawn)
    for cell in cells_to_add:
        game_state.add_cell(0,0,cell)
    game_state.execute_fight_in_position(0,0)

    assert game_state.get_ice_spawn().get_life() == expected_life  
                                                 
                                                                              


# ######Tests para execute_fights_in_all_positions
execute_fights_params = [
    # Params: board_size, cells_to_add, expected_board_state
    ((3, 3), [
        (0, 0, IceCell(level=Level.LEVEL_1, life=18, position=(0, 0))),
        (0, 0, FireCell(level=Level.LEVEL_2, life=30, position=(0, 0))),
        (1, 0, FireCell(level=Level.LEVEL_1, life=18, position=(1, 0))),
        (1, 0, IceCell(level=Level.LEVEL_2, life=30, position=(1, 0)))
    ], [
        (0, 0, 1, FireCell),
        (1, 0, 1, IceCell)
    ]),
    ((4, 4), [
        (0, 0, IceCell(level=Level.LEVEL_1, life=18, position=(0, 0))),
        (0, 1, FireCell(level=Level.LEVEL_2, life=30, position=(0, 1))),
        (1, 0, FireCell(level=Level.LEVEL_1, life=18, position=(1, 0))),
        (1, 1, IceCell(level=Level.LEVEL_2, life=30, position=(1, 1)))
    ], [
        (0, 0, 1, IceCell),
        (0, 1, 1, FireCell),
        (1, 0, 1, FireCell),
        (1, 1, 1, IceCell)
    ]), 
        ((5, 5), [
        (0, 0, IceCell(level=Level.LEVEL_1, life=18, position=(0, 0))),
        (0, 0, FireCell(level=Level.LEVEL_1, life=20, position=(0, 0))),
        (1, 0, FireCell(level=Level.LEVEL_1, life=18, position=(1, 0))),
        (1, 0, IceCell(level=Level.LEVEL_2, life=30, position=(1, 0))), 
        (0, 0, IceCell(level=Level.LEVEL_2, life=30, position=(0, 0)))
    ], [
        (0, 0, 2, IceCell),
        (1, 0, 1, IceCell)
    ]),
        ((5, 5), [
        (0, 0, IceCell(level=Level.LEVEL_1, life=10, position=(0, 0))),
        (1, 1, FireCell(level=Level.LEVEL_2, life=30, position=(1, 1))),
    ], [
        (0, 0, 1, IceCell),
        (1, 1, 1, FireCell)
    ]),
        ((5, 5), [
        (0, 0, IceCell(level=Level.LEVEL_1, life=10, position=(0, 0))),
        (0, 0, FireCell(level=Level.LEVEL_2, life=30, position=(0, 0))),
        (1, 1, FireCell(level=Level.LEVEL_3, life=50, position=(1, 1))),
        (1, 1, IceCell(level=Level.LEVEL_2, life=40, position=(1, 1))), 
    ], [
        (0, 0, 1, FireCell),
        (1, 1, 1, FireCell)
    ]),
        ((5, 5), [
        (0, 0, IceCell(level=Level.LEVEL_1, life=15, position=(0, 0))),
        (0, 0, FireCell(level=Level.LEVEL_2, life=25, position=(0, 0))),
        (1, 0, FireCell(level=Level.LEVEL_1, life=15, position=(1, 0))),
        (1, 0, IceCell(level=Level.LEVEL_3, life=45, position=(1, 0))), 
        (0, 0, IceCell(level=Level.LEVEL_2, life=25, position=(0, 0)))
    ], [
        (0, 0, 1, FireCell),
        (1, 0, 1, IceCell)
    ])
]

@pytest.mark.parametrize("board_size, cells_to_add, expected_cells_pos", execute_fights_params)
def test_execute_fights_in_all_positions(board_size, cells_to_add, expected_cells_pos):
    game_state = GameState()
    game_state.new_game(*board_size)
    for cell_params in cells_to_add:
        row, column, cell = cell_params
        game_state.add_cell(row, column, cell)
    
    game_state.execute_fights_in_all_positions()
    for expected_cell in expected_cells_pos:
        row, column, count, type = expected_cell
        cells = game_state.get_cells(row, column)
        assert count == len(cells)
        for cell in cells:
            assert isinstance(cell, type)



############Test para movement (move_cells_in_position)
movement_params = [
    ((10, 10), [(FireCell(level=Level.LEVEL_1, life=20, position=(2,3))),
              (FireCell(level=Level.LEVEL_1, life=20, position=(2,3))),
              (FireCell(level=Level.LEVEL_1, life=20, position=(2,3)))],
               [(1, 3), (3, 3), (2, 4), (2, 2), (1, 2), (3, 4), (3, 2), (1, 4)], 19),
    ((10, 10), [(IceCell(level=Level.LEVEL_2, life=38, position=(4, 5))),
        (IceCell(level=Level.LEVEL_2, life=38, position=(4, 5))),
        (IceCell(level=Level.LEVEL_2, life=38, position=(4, 5)))
    ], [(3, 5), (5, 5), (4, 6), (4, 4), (3, 4), (5, 6), (5, 4), (3, 6)], 37),
    ((10, 10), [
        FireCell(level=Level.LEVEL_1, life=2, position=(4, 5)),
        FireCell(level=Level.LEVEL_1, life=2, position=(4, 5)),
        IceCell(level=Level.LEVEL_1, life=2, position=(4, 5)),
        IceCell(level=Level.LEVEL_1, life=2, position=(4, 5))
    ], [(3, 5), (5, 5), (4, 6), (4, 4), (3, 4), (5, 6), (5, 4), (3, 6)], 1)
]

@pytest.mark.parametrize("board_size, cells_to_add, expected_positions, expected_life_points", movement_params)
def test_movement_board(board_size, cells_to_add, expected_positions, expected_life_points):
    game_state = GameState()
    game_state.new_game(*board_size)
    pos = cells_to_add[0].get_position()
    for cell in cells_to_add:
        cell.board = game_state.get_board()
        cell.position = pos
        game_state.add_cell(*pos, cell)
    game_state.move_cells_in_position(*pos)
    for cell in cells_to_add:
        assert cell.position in expected_positions
        assert cell.life == expected_life_points
        assert cell not in game_state.get_cells(*pos)
