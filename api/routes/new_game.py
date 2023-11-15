from flask import jsonify, request, session
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
from marshmallow import ValidationError

class NewGameResource(Resource):

    def post(self):
        data = request.json

        row = data.get('row')
        column = data.get('column')
        id = data.get('game_state_id')
        # Validate row and column
        if not isinstance(row, int) or not isinstance(column, int):
            return {'message': 'Row and column must be integers'}, 400
        
        if not 0 <= row <= 13 or not 0 <= column <= 13:
            return {'message': 'Row and column must be integers between 0 and 14 '}, 422

        game_state_model = GameStateModel.query.get(id)
        if game_state_model is None:
            return {'message': 'GameState not found'}, 404

        # Convert the game_state_model to a dictionary
        game_state_data_model = game_state_model.to_dict()

        # Deserialize the game_state_data_model to a GameState object 
        logic_game_state = GameState.create_from_dict(game_state_data_model)

        # Pass the GameState object to the GameController constructor
        game_controller = GameController(logic_game_state)
        game_controller.new_game(15, 15)

        spawn_type = 'IceSpawn' if game_controller.get_team() == Team.IceTeam else 'FireSpawn'
        game_controller.create_spawn(row, column, spawn_type)

        current_game_state = game_controller.get_game_state()

        # Schemas instances to serialize
        board_schema = BoardSchema()
        spawn_schema = SpawnSchema()
        healing_area_schema = HealingAreaSchema()
        try:
            board_dict = board_schema.dump(current_game_state.board)
            ice_spawn_dict = spawn_schema.dump(current_game_state.ice_spawn)
            fire_spawn_dict = spawn_schema.dump(current_game_state.fire_spawn)
            fire_healing_area_dict = healing_area_schema.dump(current_game_state.fire_healing_area)
            ice_healing_area_dict = healing_area_schema.dump(current_game_state.ice_healing_area)
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
            ice_healing_area=json.dumps(ice_healing_area_dict),  
            fire_healing_area=json.dumps(fire_healing_area_dict)
        )

        game_state_dict = game_state_model.to_dict()
        #print(game_state_dict)
        GameStateModel.query.filter(GameStateModel.id == game_state_model.id).update(game_state_dict)

        db.session.commit()
        return {'message': 'Spawn set successfully', 'game_state': game_state_dict}, 200    

api.add_resource(NewGameResource, '/new_game')
