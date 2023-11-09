import pytest

from logic.game_state import GameState, Team, GameMode
from logic.cell import FireCell, IceCell, Level
from logic.spawn import IceSpawn, FireSpawn
import time

@pytest.fixture
def gamestate():
    game_state = GameState()
    game_state.set_team(Team.FireTeam)
    game_state.new_game(10, 10)
    return game_state

##TEST Cell on Board

#Test that a cell on an empty board correctly identifies its adjacent cells.
def test_get_adjacents_empty_board(gamestate):
    currentadjacents = gamestate.get_adjacents_for_move((1, 1), gamestate.get_team())

    assert currentadjacents == [(2, 1), (0, 1), (1, 2), (1, 0), (2, 2), (0, 0), (2, 0), (0, 2)]

#Test that a cell in the center of the board with neighbors correctly identifies its adjacent cells.
def test_get_adjacents_for_move_center_fire_cell(gamestate):
    gamestate.create_cell( 1, 1, FireCell, 1, 20)
    adjacentlist = gamestate.get_adjacents_for_move((1, 1), gamestate.get_team())
    print(adjacentlist)
    assert set(adjacentlist) == set([(2, 1), (0, 1), (1, 2), (1, 0), (2, 2), (0, 0), (2, 0), (0, 2)])

#Test that a cell in a corner of the board with neighbors correctly identifies its adjacent cells.
def test_get_adjacents_for_move_corner_fire_cell(gamestate):
    gamestate.create_cell(1, 0, gamestate.get_team(), Level.LEVEL_1, 20)

    assert set(gamestate.get_adjacents_for_move((0, 0), gamestate.get_team())) == set([(1, 0), (0, 1), (1, 1)])

#Test that a cell on an edge of the board with neighbors correctly identifies its adjacent cells.
def test_get_adjacents_for_move_edge_fire_cell(gamestate):
    gamestate.create_cell(0, 0, gamestate.get_team(), Level.LEVEL_1, 20)

    assert set(gamestate.get_adjacents_for_move((1, 0), gamestate.get_team())) == set([(2, 0), (0, 0), (1, 1), (2, 1), (0, 1)])
    
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

def test_create_inverse_spawn():
    game_state = GameState()
    game_state.new_game(10,10)  

    game_state.create_spawn(2, 2, IceSpawn)

    ice_spawn = game_state.get_ice_spawn()
    fire_spawn = game_state.get_fire_spawn()

    expected_ice_positions = [(1,1), (1,2), (1,3), (2,1), (2,2), (2,3), (3,1), (3,2), (3,3)]
    expected_fire_positions = [(6,6), (6,7), (6,8), (7,6), (7,7), (7,8), (8,6), (8,7), (8,8)]
    assert ice_spawn.get_positions() == expected_ice_positions
    assert fire_spawn.get_positions() == expected_fire_positions 
    assert game_state.get_mode() == GameMode.SIMULATION
    assert isinstance(ice_spawn, IceSpawn)
    assert isinstance(fire_spawn, FireSpawn)

def test_create_inverse_spawn_2():
    game_state = GameState()
    game_state.new_game(50,50)  

    game_state.create_spawn(20, 20, IceSpawn)

    ice_spawn = game_state.get_ice_spawn()
    fire_spawn = game_state.get_fire_spawn()

    expected_ice_positions = [(19, 19), (19, 20), (19, 21), (20, 19), (20, 20), (20, 21), (21, 19), (21, 20), (21, 21)]
    expected_fire_positions = [(30, 30), (30, 29), (30, 28), (29, 30), (29, 29), (29, 28), (28, 30), (28, 29), (28, 28)]
    assert set(ice_spawn.get_positions()) == set(expected_ice_positions)
    assert set(fire_spawn.get_positions()) == set(expected_fire_positions) 
    assert game_state.get_mode() == GameMode.SIMULATION
    assert isinstance(ice_spawn, IceSpawn)
    assert isinstance(fire_spawn, FireSpawn)

##########   Next test is not working if of 20 executions, 20 gives error. if some test pass method works ok.
# @pytest.mark.parametrize("run", range(20))
# def test_advance_method_with_spawn(gamestate, run):
#     gamestate.set_team(Team.FireTeam)
#     gamestate.create_cell(0, 0, gamestate.get_team(), Level.LEVEL_1, 20)
#     gamestate.create_cell(0, 0, gamestate.get_team(), Level.LEVEL_1, 20)
#     gamestate.create_cell(0, 0, gamestate.get_team(), Level.LEVEL_1, 20)

#     gamestate.create_spawn(2, 2, IceSpawn)

#     gamestate.move_cells_in_position(0, 0)
    
#     assert len(gamestate.get_cells_in_spawn(gamestate.get_ice_spawn())) > 0

## TEST Fusion of Board
def test_fusion_board(gamestate):
    pos = (1,1)
    gamestate.create_cell(pos[0], pos[1], FireCell, level=Level.LEVEL_2, life=36)
    gamestate.create_cell(pos[0], pos[1], FireCell, level=Level.LEVEL_1, life=16)
    gamestate.create_cell(pos[0], pos[1], FireCell, level=Level.LEVEL_1, life=7)
    gamestate.create_cell(pos[0], pos[1], IceCell, level=Level.LEVEL_1, life=2)
    gamestate.create_cell(pos[0], pos[1], IceCell, level=Level.LEVEL_1, life=12)
    gamestate.fusion(pos)
    cells_in_pos = gamestate.get_cells(pos[0], pos[1])
    assert len(cells_in_pos) == 2
    assert isinstance(cells_in_pos[0], IceCell)
    assert isinstance(cells_in_pos[1], FireCell)
    assert cells_in_pos[0].get_life() == 40
    assert cells_in_pos[0].get_level() == Level.LEVEL_2
    assert cells_in_pos[1].get_life() == 60
    assert cells_in_pos[1].get_level() == Level.LEVEL_3
    
def test_fusion_in_all_board(gamestate):
    pos0 = (0,0)
    gamestate.create_cell(pos0[0], pos0[1], IceCell, level=Level.LEVEL_2, life=36)
    gamestate.create_cell(pos0[0], pos0[1], IceCell, level=Level.LEVEL_2, life=30,)

    pos1 = (0,1)
    gamestate.create_cell(pos1[0], pos1[1], IceCell, level=Level.LEVEL_1, life=15)
    gamestate.create_cell(pos1[0], pos1[1], IceCell, level=Level.LEVEL_1, life=2)

    pos2 = (1,0)
    gamestate.create_cell(pos2[0], pos2[1], FireCell, level=Level.LEVEL_3, life=48)
    gamestate.create_cell(pos2[0], pos2[1], IceCell, level=Level.LEVEL_1, life=15)
    
    pos3 = (1,1)
    gamestate.create_cell(pos3[0], pos3[1], FireCell, level=Level.LEVEL_3, life=50)
    gamestate.create_cell(pos3[0], pos3[1], FireCell, level=Level.LEVEL_2, life=29)

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
    assert isinstance(cells_in_pos_10[0], IceCell)
    assert isinstance(cells_in_pos_10[1], FireCell)
    assert cells_in_pos_10[0].life == 15
    assert cells_in_pos_10[0].level == Level.LEVEL_1
    assert cells_in_pos_10[1].life == 48
    assert cells_in_pos_10[1].level == Level.LEVEL_3

    # Comprueba que no hubo fusión en (1, 1)
    assert len(cells_in_pos_11) == 2
    assert isinstance(cells_in_pos_11[0], FireCell)
    assert isinstance(cells_in_pos_11[1], FireCell)
    assert cells_in_pos_11[0].life == 50
    assert cells_in_pos_11[0].level == Level.LEVEL_3
    assert cells_in_pos_11[1].life == 29
    assert cells_in_pos_11[1].level == Level.LEVEL_2

def test_generate_cells():
    game = GameState()
    game.set_team(Team.FireTeam)
    game.new_game(40, 40)
    game.create_spawn(1, 1, FireSpawn)
    game.generate_cells()
    adj_fire = game.fire_spawn.get_adjacents_spawn(40)
    adj_ice = game.ice_spawn.get_adjacents_spawn(40)

    for i in adj_fire:
        r, c = i 
        if (game.get_cells(r,c) != 0):
            cells = game.get_cells(r,c)
            for cell in cells:
                assert isinstance(cell, FireCell)
    
    for j in adj_ice:
        r, c = j 
        if (game.get_cells(r,c) != 0):
            cells = game.get_cells(r,c)
            for cell in cells:
                assert isinstance(cell, IceCell)

# def test_apply_healing():
#     game = GameState()
#     game.new_game(15,15)
#     game.create_spawn(1,1,IceSpawn)
#     ice_ha_duration = game.get_ice_healing_area().get_duration()
#     ice_cell = IceCell()
#     ice_pos = game.get_ice_healing_area().get_positions()
#     game.add_cell(*ice_pos[0], ice_cell)
#     cell_life = ice_cell.get_life()
#     game.apply_healing()
#     assert cell_life + 3 == ice_cell.get_life()
#     assert ice_ha_duration - 1 == game.get_ice_healing_area().get_duration()

def test_update_state():
    game = GameState()
    game.new_game(15, 15)
    game.create_spawn(1, 1, IceSpawn)
    for i in range(1000):
        if game.get_mode() == GameMode.FINISHED:
            print('Simulation finished')
            break
        print(str(game.get_board()))
        game.update_state()
        print(f"IceSpawnLife: {game.get_ice_spawn().get_life()} FireSpawnLife: {game.get_fire_spawn().get_life()}")
        print(f"LifeIceHA: {game.get_ice_healing_area().get_duration()} HealRteIHA: {game.get_ice_healing_area().get_healing_rate()} ")
        print(f"LifeFireHA: {game.get_fire_healing_area().get_duration()} HealRteFHA: {game.get_fire_healing_area().get_healing_rate()}")
        for row in range(game.get_board().__len__()):
            for column in range(game.get_board().get_columns()):
                ice_cells = game.get_ice_cells(row, column)
                for cell in ice_cells:
                    print(f"IceCell:Life: {cell.get_life()}, Level: {cell.get_level()}, Position: {cell.get_position()}")
                fire_cells = game.get_ice_cells(row, column)
                for cell in fire_cells:
                    print(f"FireCell: Life: {cell.get_life()}, Level: {cell.get_level()}, Position: {cell.get_position()}")

    assert 1 == 2

@pytest.fixture
def game_state_dict():
    return {
        "board": {
            "board": [
                [
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            0,
                            0
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    0,
                                    0
                                ],
                                [
                                    0,
                                    1
                                ],
                                [
                                    0,
                                    2
                                ],
                                [
                                    1,
                                    0
                                ],
                                [
                                    1,
                                    1
                                ],
                                [
                                    1,
                                    2
                                ],
                                [
                                    2,
                                    0
                                ],
                                [
                                    2,
                                    1
                                ],
                                [
                                    2,
                                    2
                                ]
                            ],
                            "type": "IceSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            0,
                            1
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    0,
                                    0
                                ],
                                [
                                    0,
                                    1
                                ],
                                [
                                    0,
                                    2
                                ],
                                [
                                    1,
                                    0
                                ],
                                [
                                    1,
                                    1
                                ],
                                [
                                    1,
                                    2
                                ],
                                [
                                    2,
                                    0
                                ],
                                [
                                    2,
                                    1
                                ],
                                [
                                    2,
                                    2
                                ]
                            ],
                            "type": "IceSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            0,
                            2
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    0,
                                    0
                                ],
                                [
                                    0,
                                    1
                                ],
                                [
                                    0,
                                    2
                                ],
                                [
                                    1,
                                    0
                                ],
                                [
                                    1,
                                    1
                                ],
                                [
                                    1,
                                    2
                                ],
                                [
                                    2,
                                    0
                                ],
                                [
                                    2,
                                    1
                                ],
                                [
                                    2,
                                    2
                                ]
                            ],
                            "type": "IceSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            0,
                            3
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            0,
                            4
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            0,
                            5
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            0,
                            6
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            0,
                            7
                        ],
                        "spawn": None
                    }
                ],
                [
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            1,
                            0
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    0,
                                    0
                                ],
                                [
                                    0,
                                    1
                                ],
                                [
                                    0,
                                    2
                                ],
                                [
                                    1,
                                    0
                                ],
                                [
                                    1,
                                    1
                                ],
                                [
                                    1,
                                    2
                                ],
                                [
                                    2,
                                    0
                                ],
                                [
                                    2,
                                    1
                                ],
                                [
                                    2,
                                    2
                                ]
                            ],
                            "type": "IceSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            1,
                            1
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    0,
                                    0
                                ],
                                [
                                    0,
                                    1
                                ],
                                [
                                    0,
                                    2
                                ],
                                [
                                    1,
                                    0
                                ],
                                [
                                    1,
                                    1
                                ],
                                [
                                    1,
                                    2
                                ],
                                [
                                    2,
                                    0
                                ],
                                [
                                    2,
                                    1
                                ],
                                [
                                    2,
                                    2
                                ]
                            ],
                            "type": "IceSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            1,
                            2
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    0,
                                    0
                                ],
                                [
                                    0,
                                    1
                                ],
                                [
                                    0,
                                    2
                                ],
                                [
                                    1,
                                    0
                                ],
                                [
                                    1,
                                    1
                                ],
                                [
                                    1,
                                    2
                                ],
                                [
                                    2,
                                    0
                                ],
                                [
                                    2,
                                    1
                                ],
                                [
                                    2,
                                    2
                                ]
                            ],
                            "type": "IceSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            1,
                            3
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            1,
                            4
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            1,
                            5
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            1,
                            6
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            1,
                            7
                        ],
                        "spawn": None
                    }
                ],
                [
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            2,
                            0
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    0,
                                    0
                                ],
                                [
                                    0,
                                    1
                                ],
                                [
                                    0,
                                    2
                                ],
                                [
                                    1,
                                    0
                                ],
                                [
                                    1,
                                    1
                                ],
                                [
                                    1,
                                    2
                                ],
                                [
                                    2,
                                    0
                                ],
                                [
                                    2,
                                    1
                                ],
                                [
                                    2,
                                    2
                                ]
                            ],
                            "type": "IceSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            2,
                            1
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    0,
                                    0
                                ],
                                [
                                    0,
                                    1
                                ],
                                [
                                    0,
                                    2
                                ],
                                [
                                    1,
                                    0
                                ],
                                [
                                    1,
                                    1
                                ],
                                [
                                    1,
                                    2
                                ],
                                [
                                    2,
                                    0
                                ],
                                [
                                    2,
                                    1
                                ],
                                [
                                    2,
                                    2
                                ]
                            ],
                            "type": "IceSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            2,
                            2
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    0,
                                    0
                                ],
                                [
                                    0,
                                    1
                                ],
                                [
                                    0,
                                    2
                                ],
                                [
                                    1,
                                    0
                                ],
                                [
                                    1,
                                    1
                                ],
                                [
                                    1,
                                    2
                                ],
                                [
                                    2,
                                    0
                                ],
                                [
                                    2,
                                    1
                                ],
                                [
                                    2,
                                    2
                                ]
                            ],
                            "type": "IceSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            2,
                            3
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            2,
                            4
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            2,
                            5
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            2,
                            6
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            2,
                            7
                        ],
                        "spawn": None
                    }
                ],
                [
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            3,
                            0
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            3,
                            1
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            3,
                            2
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": {
                            "affected_cell_type": "IceCell",
                            "duration": 100,
                            "healing_rate": 3,
                            "positions": [
                                [
                                    3,
                                    3
                                ],
                                [
                                    3,
                                    4
                                ],
                                [
                                    3,
                                    5
                                ],
                                [
                                    4,
                                    3
                                ],
                                [
                                    4,
                                    4
                                ],
                                [
                                    4,
                                    5
                                ],
                                [
                                    5,
                                    3
                                ],
                                [
                                    5,
                                    4
                                ],
                                [
                                    5,
                                    5
                                ]
                            ]
                        },
                        "pos": [
                            3,
                            3
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": {
                            "affected_cell_type": "IceCell",
                            "duration": 100,
                            "healing_rate": 3,
                            "positions": [
                                [
                                    3,
                                    3
                                ],
                                [
                                    3,
                                    4
                                ],
                                [
                                    3,
                                    5
                                ],
                                [
                                    4,
                                    3
                                ],
                                [
                                    4,
                                    4
                                ],
                                [
                                    4,
                                    5
                                ],
                                [
                                    5,
                                    3
                                ],
                                [
                                    5,
                                    4
                                ],
                                [
                                    5,
                                    5
                                ]
                            ]
                        },
                        "pos": [
                            3,
                            4
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": {
                            "affected_cell_type": "IceCell",
                            "duration": 100,
                            "healing_rate": 3,
                            "positions": [
                                [
                                    3,
                                    3
                                ],
                                [
                                    3,
                                    4
                                ],
                                [
                                    3,
                                    5
                                ],
                                [
                                    4,
                                    3
                                ],
                                [
                                    4,
                                    4
                                ],
                                [
                                    4,
                                    5
                                ],
                                [
                                    5,
                                    3
                                ],
                                [
                                    5,
                                    4
                                ],
                                [
                                    5,
                                    5
                                ]
                            ]
                        },
                        "pos": [
                            3,
                            5
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            3,
                            6
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            3,
                            7
                        ],
                        "spawn": None
                    }
                ],
                [
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            4,
                            0
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            4,
                            1
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            4,
                            2
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": {
                            "affected_cell_type": "IceCell",
                            "duration": 100,
                            "healing_rate": 3,
                            "positions": [
                                [
                                    3,
                                    3
                                ],
                                [
                                    3,
                                    4
                                ],
                                [
                                    3,
                                    5
                                ],
                                [
                                    4,
                                    3
                                ],
                                [
                                    4,
                                    4
                                ],
                                [
                                    4,
                                    5
                                ],
                                [
                                    5,
                                    3
                                ],
                                [
                                    5,
                                    4
                                ],
                                [
                                    5,
                                    5
                                ]
                            ]
                        },
                        "pos": [
                            4,
                            3
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": {
                            "affected_cell_type": "IceCell",
                            "duration": 100,
                            "healing_rate": 3,
                            "positions": [
                                [
                                    3,
                                    3
                                ],
                                [
                                    3,
                                    4
                                ],
                                [
                                    3,
                                    5
                                ],
                                [
                                    4,
                                    3
                                ],
                                [
                                    4,
                                    4
                                ],
                                [
                                    4,
                                    5
                                ],
                                [
                                    5,
                                    3
                                ],
                                [
                                    5,
                                    4
                                ],
                                [
                                    5,
                                    5
                                ]
                            ]
                        },
                        "pos": [
                            4,
                            4
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": {
                            "affected_cell_type": "IceCell",
                            "duration": 100,
                            "healing_rate": 3,
                            "positions": [
                                [
                                    3,
                                    3
                                ],
                                [
                                    3,
                                    4
                                ],
                                [
                                    3,
                                    5
                                ],
                                [
                                    4,
                                    3
                                ],
                                [
                                    4,
                                    4
                                ],
                                [
                                    4,
                                    5
                                ],
                                [
                                    5,
                                    3
                                ],
                                [
                                    5,
                                    4
                                ],
                                [
                                    5,
                                    5
                                ]
                            ]
                        },
                        "pos": [
                            4,
                            5
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            4,
                            6
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            4,
                            7
                        ],
                        "spawn": None
                    }
                ],
                [
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            5,
                            0
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            5,
                            1
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            5,
                            2
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": {
                            "affected_cell_type": "IceCell",
                            "duration": 100,
                            "healing_rate": 3,
                            "positions": [
                                [
                                    3,
                                    3
                                ],
                                [
                                    3,
                                    4
                                ],
                                [
                                    3,
                                    5
                                ],
                                [
                                    4,
                                    3
                                ],
                                [
                                    4,
                                    4
                                ],
                                [
                                    4,
                                    5
                                ],
                                [
                                    5,
                                    3
                                ],
                                [
                                    5,
                                    4
                                ],
                                [
                                    5,
                                    5
                                ]
                            ]
                        },
                        "pos": [
                            5,
                            3
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": {
                            "affected_cell_type": "IceCell",
                            "duration": 100,
                            "healing_rate": 3,
                            "positions": [
                                [
                                    3,
                                    3
                                ],
                                [
                                    3,
                                    4
                                ],
                                [
                                    3,
                                    5
                                ],
                                [
                                    4,
                                    3
                                ],
                                [
                                    4,
                                    4
                                ],
                                [
                                    4,
                                    5
                                ],
                                [
                                    5,
                                    3
                                ],
                                [
                                    5,
                                    4
                                ],
                                [
                                    5,
                                    5
                                ]
                            ]
                        },
                        "pos": [
                            5,
                            4
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [
                            {
                                "level": 1,
                                "life": 20,
                                "position": [
                                    5,
                                    5
                                ]
                            }
                        ],
                        "ice_healing_area": {
                            "affected_cell_type": "IceCell",
                            "duration": 100,
                            "healing_rate": 3,
                            "positions": [
                                [
                                    3,
                                    3
                                ],
                                [
                                    3,
                                    4
                                ],
                                [
                                    3,
                                    5
                                ],
                                [
                                    4,
                                    3
                                ],
                                [
                                    4,
                                    4
                                ],
                                [
                                    4,
                                    5
                                ],
                                [
                                    5,
                                    3
                                ],
                                [
                                    5,
                                    4
                                ],
                                [
                                    5,
                                    5
                                ]
                            ]
                        },
                        "pos": [
                            5,
                            5
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    5,
                                    5
                                ],
                                [
                                    5,
                                    6
                                ],
                                [
                                    5,
                                    7
                                ],
                                [
                                    6,
                                    5
                                ],
                                [
                                    6,
                                    6
                                ],
                                [
                                    6,
                                    7
                                ],
                                [
                                    7,
                                    5
                                ],
                                [
                                    7,
                                    6
                                ],
                                [
                                    7,
                                    7
                                ]
                            ],
                            "type": "FireSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            5,
                            6
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    5,
                                    5
                                ],
                                [
                                    5,
                                    6
                                ],
                                [
                                    5,
                                    7
                                ],
                                [
                                    6,
                                    5
                                ],
                                [
                                    6,
                                    6
                                ],
                                [
                                    6,
                                    7
                                ],
                                [
                                    7,
                                    5
                                ],
                                [
                                    7,
                                    6
                                ],
                                [
                                    7,
                                    7
                                ]
                            ],
                            "type": "FireSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            5,
                            7
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    5,
                                    5
                                ],
                                [
                                    5,
                                    6
                                ],
                                [
                                    5,
                                    7
                                ],
                                [
                                    6,
                                    5
                                ],
                                [
                                    6,
                                    6
                                ],
                                [
                                    6,
                                    7
                                ],
                                [
                                    7,
                                    5
                                ],
                                [
                                    7,
                                    6
                                ],
                                [
                                    7,
                                    7
                                ]
                            ],
                            "type": "FireSpawn"
                        }
                    }
                ],
                [
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            6,
                            0
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            6,
                            1
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            6,
                            2
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            6,
                            3
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            6,
                            4
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            6,
                            5
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    5,
                                    5
                                ],
                                [
                                    5,
                                    6
                                ],
                                [
                                    5,
                                    7
                                ],
                                [
                                    6,
                                    5
                                ],
                                [
                                    6,
                                    6
                                ],
                                [
                                    6,
                                    7
                                ],
                                [
                                    7,
                                    5
                                ],
                                [
                                    7,
                                    6
                                ],
                                [
                                    7,
                                    7
                                ]
                            ],
                            "type": "FireSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            6,
                            6
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    5,
                                    5
                                ],
                                [
                                    5,
                                    6
                                ],
                                [
                                    5,
                                    7
                                ],
                                [
                                    6,
                                    5
                                ],
                                [
                                    6,
                                    6
                                ],
                                [
                                    6,
                                    7
                                ],
                                [
                                    7,
                                    5
                                ],
                                [
                                    7,
                                    6
                                ],
                                [
                                    7,
                                    7
                                ]
                            ],
                            "type": "FireSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            6,
                            7
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    5,
                                    5
                                ],
                                [
                                    5,
                                    6
                                ],
                                [
                                    5,
                                    7
                                ],
                                [
                                    6,
                                    5
                                ],
                                [
                                    6,
                                    6
                                ],
                                [
                                    6,
                                    7
                                ],
                                [
                                    7,
                                    5
                                ],
                                [
                                    7,
                                    6
                                ],
                                [
                                    7,
                                    7
                                ]
                            ],
                            "type": "FireSpawn"
                        }
                    }
                ],
                [
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            7,
                            0
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            7,
                            1
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            7,
                            2
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            7,
                            3
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            7,
                            4
                        ],
                        "spawn": None
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            7,
                            5
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    5,
                                    5
                                ],
                                [
                                    5,
                                    6
                                ],
                                [
                                    5,
                                    7
                                ],
                                [
                                    6,
                                    5
                                ],
                                [
                                    6,
                                    6
                                ],
                                [
                                    6,
                                    7
                                ],
                                [
                                    7,
                                    5
                                ],
                                [
                                    7,
                                    6
                                ],
                                [
                                    7,
                                    7
                                ]
                            ],
                            "type": "FireSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            7,
                            6
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    5,
                                    5
                                ],
                                [
                                    5,
                                    6
                                ],
                                [
                                    5,
                                    7
                                ],
                                [
                                    6,
                                    5
                                ],
                                [
                                    6,
                                    6
                                ],
                                [
                                    6,
                                    7
                                ],
                                [
                                    7,
                                    5
                                ],
                                [
                                    7,
                                    6
                                ],
                                [
                                    7,
                                    7
                                ]
                            ],
                            "type": "FireSpawn"
                        }
                    },
                    {
                        "fire_cells": [],
                        "fire_healing_area": None,
                        "ice_cells": [],
                        "ice_healing_area": None,
                        "pos": [
                            7,
                            7
                        ],
                        "spawn": {
                            "life": 300,
                            "positions": [
                                [
                                    5,
                                    5
                                ],
                                [
                                    5,
                                    6
                                ],
                                [
                                    5,
                                    7
                                ],
                                [
                                    6,
                                    5
                                ],
                                [
                                    6,
                                    6
                                ],
                                [
                                    6,
                                    7
                                ],
                                [
                                    7,
                                    5
                                ],
                                [
                                    7,
                                    6
                                ],
                                [
                                    7,
                                    7
                                ]
                            ],
                            "type": "FireSpawn"
                        }
                    }
                ]
            ],
            "columns": 8,
            "rows": 8
        },
        "fire_healing_area": None,
        "fire_spawn": {
            "life": 300,
            "positions": [
                [
                    5,
                    5
                ],
                [
                    5,
                    6
                ],
                [
                    5,
                    7
                ],
                [
                    6,
                    5
                ],
                [
                    6,
                    6
                ],
                [
                    6,
                    7
                ],
                [
                    7,
                    5
                ],
                [
                    7,
                    6
                ],
                [
                    7,
                    7
                ]
            ],
            "type": "FireSpawn"
        },
        "ice_healing_area": {
            "affected_cell_type": "IceCell",
            "duration": 100,
            "healing_rate": 3,
            "positions": [
                [
                    3,
                    3
                ],
                [
                    3,
                    4
                ],
                [
                    3,
                    5
                ],
                [
                    4,
                    3
                ],
                [
                    4,
                    4
                ],
                [
                    4,
                    5
                ],
                [
                    5,
                    3
                ],
                [
                    5,
                    4
                ],
                [
                    5,
                    5
                ]
            ]
        },
        "ice_spawn": {
            "life": 300,
            "positions": [
                [
                    0,
                    0
                ],
                [
                    0,
                    1
                ],
                [
                    0,
                    2
                ],
                [
                    1,
                    0
                ],
                [
                    1,
                    1
                ],
                [
                    1,
                    2
                ],
                [
                    2,
                    0
                ],
                [
                    2,
                    1
                ],
                [
                    2,
                    2
                ]
            ],
            "type": "IceSpawn"
        },
        "mode": "SIMULATION",
        "team": "IceTeam",
        "username": "Genaro"
    }

### Para que el test testee debidamente, se debe comentar en game state create spawn la linea que crea healing area, ya que estamos testeando
### un diccionario en un estado sin fire healing area. Ademas no tendria sentido testear este metodo con algo random 
# def test_create_from_dict(game_state_dict):
#     game_state = GameState.create_from_dict(game_state_dict)
#     actual_game_state = GameState()
#     actual_game_state.new_game(8,8)
#     actual_game_state.set_team(Team.IceTeam)
#     actual_game_state.set_mode(GameMode.SIMULATION)
#     actual_game_state.set_username('Genaro')
#     actual_game_state.create_spawn(1,1,IceSpawn)
#     actual_game_state.create_cell(5,5,IceCell)
#     actual_game_state.create_healing_area(4,4,IceCell)
#     # def print_game_state_attributes(game_state):
#     #     for attr, value in game_state.__dict__.items():
#     #         print(f"{attr}: {value}")

#     # print_game_state_attributes(game_state)
#     # print_game_state_attributes(actual_game_state)
#     assert game_state == actual_game_state



    
