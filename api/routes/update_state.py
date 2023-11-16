from flask import jsonify, request
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


class UpdateStateResource(Resource):
    def post(self):
        data = request.json
        game_state_id = data.get('id')
        game_state_model = GameStateModel.query.get(game_state_id)

        if game_state_model is None:
            return {'message': 'GameState not found'}, 404
        
        game_state_data_model = game_state_model.to_dict()
        logic_game_state = GameState.create_from_dict(game_state_data_model)
        
        if logic_game_state.get_ice_spawn() is None:
            return {'message': 'Spawn was not setted'}, 400
        
        game_controller = GameController(logic_game_state)
        game_controller.update_state()

        current_game_state = game_controller.get_game_state()

        current_board_str = str(game_controller.get_game_state().get_board())

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
            print(f"Error during deserialization: {err.messages}")
            return {'message': 'Error during deserialization'}, 500

        # Actualizar los atributos de la instancia existente con los valores actualizados
        game_state_model.team = current_game_state.team.value
        game_state_model.mode = current_game_state.mode.value
        game_state_model.board = json.dumps(board_dict)
        game_state_model.ice_spawn = json.dumps(ice_spawn_dict)
        game_state_model.fire_spawn = json.dumps(fire_spawn_dict)
        game_state_model.ice_healing_area = json.dumps(ice_healing_area_dict)
        game_state_model.fire_healing_area = json.dumps(fire_healing_area_dict)

        # Convert the GameStateModel instance to a dictionary to see updated game state in the response
        game_state_dict = game_state_model.to_dict()
        GameStateModel.query.filter(GameStateModel.id == game_state_model.id).update(game_state_dict)
        db.session.commit()
        return {'updated_game_state': game_state_dict, 'board_str': current_board_str}, 200 
api.add_resource(UpdateStateResource, '/update_state')

