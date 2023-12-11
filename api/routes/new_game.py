from flask import request, session
from flask_restful import Resource
from api.routes import api
from logic.game_state import GameState, Team
from logic.game_controller import GameController
from app.models.game_state_model import GameStateModel
from app.schemas.board_schema import BoardSchema
from app.schemas.spawn_schema import SpawnSchema
from app.schemas.healing_area_schema import HealingAreaSchema
from api import db
import json
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo
class NewGameResource(Resource):

    # Handles the POST request to set a spawn in the game state.
    def post(self):
        try:
            data = request.json
            self.validate_input(data)

            row, column, row_healing_area, column_healing_area, game_state_id = data['row'], data['column'], data['row_healing_area'], data['column_healing_area'], data['game_state_id']
            game_state_model = self.get_game_state_model(game_state_id)

            game_controller = self.initialize_game_controller(game_state_model, int(data.get('size')))
            if self.is_spawn_set(game_controller):
                raise Exception('Spawn already set for this game state')
            
            spawn_type = 'IceSpawn' if game_controller.get_team() == Team.IceTeam else 'FireSpawn'
            game_controller.create_spawn(row, column, spawn_type)
            affected_cell_type = 'IceCell' if game_controller.get_team() == Team.IceTeam else 'FireCell'
            game_controller.create_healing_area(row_healing_area, column_healing_area, affected_cell_type)

            updated_game_state_model = self.update_game_state_model(game_state_model, game_controller.get_game_state())
            db.session.commit()

            return {'message': 'Spawn set successfully', 'game_state': updated_game_state_model.to_dict()}, 200

        except Exception as e:
            error_message = str(e)
            return {'message': 'Error processing the request', 'error': error_message}, 500

    # Validates the input data for the spawn request.
    def validate_input(self, data):
        row, column = data.get('row'), data.get('column')
        size = data.get('size')
        max_limit = 13 if size == 15 else 18 if size == 20 else 23
        if not isinstance(row, int) or not isinstance(column, int) or not 1 <= row <= max_limit or not 1 <= column <= max_limit:
            raise Exception(f'Row and column must be integers between 1 and {max_limit}')

    # Retrieves the game state model based on the provided ID.
    def get_game_state_model(self, game_state_id):
        game_state_model = GameStateModel.query.get(game_state_id)
        if game_state_model is None:
            raise Exception('GameState not found')
        return game_state_model

    # Initializes the game controller with the game state from the model.
    def initialize_game_controller(self, game_state_model, size):
        game_state_data_model = game_state_model.to_dict()
        logic_game_state = GameState.create_from_dict(game_state_data_model)
        game_controller = GameController(logic_game_state)
        game_controller.new_game(size, size)
        return game_controller

    # Checks if a spawn is already set in the game controller.
    def is_spawn_set(self, game_controller):
        return game_controller.get_ice_spawn() is not None or game_controller.get_fire_spawn() is not None
    
    # Updates the game state model with the current game state.
    def update_game_state_model(self, game_state_model, current_game_state):
        board_schema = BoardSchema()
        spawn_schema = SpawnSchema()
        healing_area_schema = HealingAreaSchema()

        board_dict = board_schema.dump(current_game_state.board)
        ice_spawn_dict = spawn_schema.dump(current_game_state.ice_spawn)
        fire_spawn_dict = spawn_schema.dump(current_game_state.fire_spawn)
        fire_healing_area_dict = healing_area_schema.dump(current_game_state.fire_healing_area)
        ice_healing_area_dict = healing_area_schema.dump(current_game_state.ice_healing_area)

        now_local = datetime.now(ZoneInfo('America/Argentina/Buenos_Aires'))

        game_state_dict = {
            'id': game_state_model.id,
            'username': current_game_state.username,
            'team': current_game_state.team.value,
            'mode': current_game_state.mode.value,
            'board': json.dumps(board_dict),
            'ice_spawn': json.dumps(ice_spawn_dict),
            'fire_spawn': json.dumps(fire_spawn_dict),
            'ice_healing_area': json.dumps(ice_healing_area_dict),
            'fire_healing_area': json.dumps(fire_healing_area_dict),
            'timestamp': now_local
            #'simulation_id': uuid.uuid4()
        }
        
        #save simulation id
        session['simulation_id'] = game_state_model.simulation_id
        GameStateModel.query.filter(GameStateModel.id == game_state_model.id).update(game_state_dict)
        return GameStateModel.query.get(game_state_model.id)
    
api.add_resource(NewGameResource, '/new_game')
