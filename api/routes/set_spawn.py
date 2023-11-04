from flask import jsonify, request
from flask_restful import Resource
from api.routes import api
from logic.game_state import GameState, Team
from logic.game_controller import GameController
from app.models.game_state_model import GameStateModel
from app.schemas.board_schema import BoardSchema
from app.schemas.spawn_schema import SpawnSchema
from api import db
import json
from marshmallow import ValidationError

class SetSpawnResource(Resource):

    def post(self):
        data = request.json
        data_dict = {
            'row': data.get('row'),
            'column': data.get('column'),
            'game_state_id': data.get('game_state_id')
        }
        game_state_model = GameStateModel.query.get(data_dict['game_state_id'])
        if game_state_model is None:
            return {'message': 'GameState not found'}, 404

        # Convert the game_state_model to a dictionary
        game_state_data_model = game_state_model.to_dict()
        # Deserialize the game_state_data_model to a GameState object 
        logic_game_state = GameState.create_from_dict(game_state_data_model)
        # Pass the GameState object to the GameController constructor
        game_controller = GameController(logic_game_state)

        spawn_type = 'IceSpawn' if game_controller.get_team() == Team.IceTeam else 'FireSpawn'
        game_controller.create_spawn(data_dict['row'], data_dict['column'], spawn_type)

        current_game_state = game_controller.get_game_state()
        # Schemas instances to serialize
        board_schema = BoardSchema()
        spawn_schema = SpawnSchema()
        try:
            # Serialize 
            board_dict = board_schema.dump(current_game_state.board)
            ice_spawn_dict = spawn_schema.dump(current_game_state.ice_spawn)
            fire_spawn_dict = spawn_schema.dump(current_game_state.fire_spawn)
        except ValidationError as err:
            print(err.messages)
            return None

        # Convert logic game state a model game state
        game_state_model = GameStateModel(
            id=data.get('game_state_id'),
            username=current_game_state.username,
            team=current_game_state.team.value,  
            mode=current_game_state.mode.value,  
            board=json.dumps(board_dict),
            ice_spawn=json.dumps(ice_spawn_dict),
            fire_spawn=json.dumps(fire_spawn_dict),
            ice_healing_area=current_game_state.ice_healing_area,  
            fire_healing_area=current_game_state.fire_healing_area 
        )

        # Convert the GameStateModel instance to a dictionary to see updated game state in the response
        game_state_dict = game_state_model.to_dict()

        return {'message': 'Spawn set successfully', 'game_state': game_state_dict}, 200    

    
api.add_resource(SetSpawnResource, '/set_spawn')
