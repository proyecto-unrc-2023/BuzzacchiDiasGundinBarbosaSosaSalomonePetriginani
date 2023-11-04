from flask import jsonify, request
from flask_restful import Resource
from app.schemas.board_schema import BoardSchema
from app.models.board_model import BoardModel
from api.routes import api
from logic.board import Board
from logic.spawn import IceSpawn
from logic.cell import IceCell
from logic.game_controller import GameController
from api import db
import json
from app.schemas.game_state_schema import GameStateSchema
from app.models.game_state_model import GameStateModel
from logic.game_state import GameState

class BoardResource(Resource):
    def get(self):
        board_schema = BoardSchema()
        board = Board(2,2)
        board_json = board_schema.dump(board)

        return jsonify(board_json)

    # def get(self):
    #     board = Board(2,2)
    #     board_json = board.serialize_board()
    #     return board_json
    def post(self):
        data = request.json

        board_data = {
            'rows': data.get('rows'),
            'columns': data.get('columns'),
            'board': data.get('board')
        }

        board_schema = BoardSchema()
        logic_board = Board(**board_schema.load(board_data))

        # Convertir logic Board a Board Model
        api_board = BoardModel(
            rows=logic_board.rows,
            columns=logic_board.columns,
            board=json.dumps(logic_board.board)  
        )

        db.session.add(api_board)
        db.session.commit()

        api_board_dict = {
            'id': api_board.id,
            'rows': api_board.rows,
            'columns': api_board.columns,
            'board': api_board.board
        }

        return jsonify(api_board_dict)
    
api.add_resource(BoardResource, '/board')

# Hit endpoint with, and first board will be added to the DB:
# {
#     "board": [
#         [
#             {
#                 "spawn": {
#                     "life": 300,
#                     "positions": [[0, 0],[0, 1],[0, 2],[1, 0],[1, 1],[1, 2],[2, 0],[2, 1],[2, 2]],
#                     "type": "IceSpawn"
#                 },
#                 "fire_cells": [
#                     {
#                         "level": 1,
#                         "life": 18,
#                         "position": [0, 0]
#                     }
#                 ],
#                 "ice_cells": [],
#                 "fire_healing_area": null,
#                 "ice_healing_area": null,
#                 "pos": [0, 0]
#             },
#             {
#                 "spawn": null,
#                 "fire_cells": [],
#                 "ice_cells": [],
#                 "fire_healing_area": null,
#                 "ice_healing_area": null,
#                 "pos": [0, 1]
#             }
#         ],
#         [
#             {
#                 "spawn": null,
#                 "fire_cells": [],
#                 "ice_cells": [],
#                 "fire_healing_area": null,
#                 "ice_healing_area": null,
#                 "pos": [1, 0]
#             },
#             {
#                 "spawn": null,
#                 "fire_cells": [],
#                 "ice_cells": [],
#                 "fire_healing_area": null,
#                 "ice_healing_area": {
#                     "positions": [[0, 0],[0, 1],[0, 2],[1, 0],[1, 1],[1, 2],[2, 0],[2, 1],[2, 2]],
#                     "duration": 100,
#                     "healing_rate": 3
#                 },
#                 "pos": [1, 1]
#             }
#         ]
#     ],
#     "columns": 2,
#     "rows": 2
# }

class GameStateResource(Resource):
    def get(self):
        game_state_schema = GameStateSchema()
        game_state = GameState()
        game_state.new_game(8,8)
        game_state.create_spawn(1,1,IceSpawn)
        game_state.create_healing_area(4,4, IceCell)
        game_state.create_cell(5,5,IceCell)
        game_state_json = game_state_schema.dump(game_state)
        string_board = str(game_state.get_board())
        print(string_board)
        return jsonify(game_state_json, string_board)
    
    def post(self):
        data = request.json

        game_state_data = {
            'board': data.get('board'),
            'ice_spawn': data.get('ice_spawn'),
            'fire_spawn': data.get('fire_spawn'),
            'team': data.get('team'),
            'mode': data.get('mode'),
            'username': data.get('username'),
            'ice_healing_area': data.get('ice_healing_area'),
            'fire_healing_area': data.get('fire_healing_area')
        }
        game_state_schema = GameStateSchema()
        logic_game_state = GameState(**game_state_schema.load(game_state_data))

        api_game_state = GameStateModel(
            username = logic_game_state.username,
            team = logic_game_state.team.to_json(),
            mode = logic_game_state.mode.to_json(),
            fire_spawn = json.dumps(logic_game_state.fire_spawn),
            ice_spawn = json.dumps(logic_game_state.ice_spawn),
            ice_healing_area = json.dumps(logic_game_state.ice_healing_area),
            fire_healing_area = json.dumps(logic_game_state.fire_healing_area),
            board=json.dumps(logic_game_state.board)  
        )

        db.session.add(api_game_state)
        db.session.commit()

        api_game_state_dict = {
            'id': api_game_state.id,
            'username': api_game_state.username,
            'team': api_game_state.team,
            'mode': api_game_state.mode,
            'fire_spawn': api_game_state.fire_spawn,
            'ice_spawn': api_game_state.ice_spawn,
            'ice_healing_area': api_game_state.ice_healing_area,
            'fire_healing_area': api_game_state.fire_healing_area,
            'board': api_game_state.board
        }

        return jsonify(api_game_state_dict)
    
api.add_resource(GameStateResource, '/game_state')

# Hit endpoint with, and game_state will be added to DB
# {
#         "board": {
#             "rows": 2,
#             "columns": 2,
#             "board": [
#                 [
#                     {
#                         "spawn": {
#                             "life": 300,
#                             "positions": [[0, 0],[0, 1],[0, 2],[1, 0],[1, 1],[1, 2],[2, 0],[2, 1],[2, 2]],
#                             "type": "IceSpawn"
#                         },
#                         "fire_cells": [
#                             {
#                                 "level": 1,
#                                 "life": 18,
#                                 "position": [0, 0]
#                             }
#                         ],
#                         "ice_cells": [],
#                         "fire_healing_area": null,
#                         "ice_healing_area": null,
#                         "pos": [0, 0]
#                     },
#                     {
#                         "spawn": null,
#                         "fire_cells": [],
#                         "ice_cells": [],
#                         "fire_healing_area": null,
#                         "ice_healing_area": null,
#                         "pos": [0, 1]
#                     }
#                 ],
#                 [
#                     {
#                         "spawn": null,
#                         "fire_cells": [],
#                         "ice_cells": [],
#                         "fire_healing_area": null,
#                         "ice_healing_area": null,
#                         "pos": [1, 0]
#                     },
#                     {
#                         "spawn": null,
#                         "fire_cells": [],
#                         "ice_cells": [],
#                         "fire_healing_area": null,
#                         "ice_healing_area": {
#                             "positions": [[0, 0],[0, 1],[0, 2],[1, 0],[1, 1],[1, 2],[2, 0],[2, 1],[2, 2]],
#                             "duration": 100,
#                             "healing_rate": 3
#                         },
#                         "pos": [1, 1]
#                     }
#                 ]
#             ]
#         },
#         "ice_spawn": { 
#                         "life": 300,
#                         "positions": [[0, 0],[0, 1],[0, 2],[1, 0],[1, 1],[1, 2],[2, 0],[2, 1],[2, 2]],
#                         "type": "IceSpawn"
#                      },
#         "team": "IceTeam",
#         "mode": "SPAWN_PLACEMENT",
#         "username": "Genaro",
#         "ice_healing_area":{
#                             "positions": [[0, 0],[0, 1],[0, 2],[1, 0],[1, 1],[1, 2],[2, 0],[2, 1],[2, 2]],
#                             "duration": 100,
#                             "healing_rate": 3
#                            }

# }
