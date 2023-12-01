from flask import request, session
from flask_restful import Resource
from api.routes import api
from logic.game_state import GameState
from logic.game_controller import GameController
from app.models.game_state_model import GameStateModel
from app.schemas.board_schema import BoardSchema
from app.schemas.spawn_schema import SpawnSchema
from app.schemas.healing_area_schema import HealingAreaSchema
from api import db
import json
from marshmallow import ValidationError
from datetime import datetime
from sqlalchemy import desc

class UpdateStateResource(Resource):

    def post(self):
        data = request.json
        game_state_model = self.get_game_state_model(data['simulation_id'])
        if game_state_model is None:
            return {'message': 'GameState not found'}, 404

        game_state_data_model = game_state_model.to_dict()
        logic_game_state = GameState.create_from_dict(game_state_data_model)

        if logic_game_state.get_ice_spawn() is None:
            return {'message': 'Spawn was not setted'}, 400

        game_controller = self.update_game_state(logic_game_state)
        current_game_state = game_controller.get_game_state()

        serialized_data = self.serialize_game_state(current_game_state)
        if serialized_data is None:
            return {'message': 'Error during deserialization'}, 500

        new_game_state_model = self.create_new_game_state_model(current_game_state, serialized_data, game_state_data_model.get('simulation_id'))
        db.session.add(new_game_state_model)

        game_state_dict = new_game_state_model.to_dict()

        db.session.commit()
        return {'updated_game_state': game_state_dict}, 200


    def get_game_state_model(self, simulation_id):
        return GameStateModel.query.filter_by(simulation_id=simulation_id).order_by(desc(GameStateModel.timestamp)).first()

    def update_game_state(self, logic_game_state):
        game_controller = GameController(logic_game_state)
        game_controller.update_state()
        return game_controller

    def serialize_game_state(self, current_game_state):
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
            return None
        return {
            'board': board_dict,
            'ice_spawn': ice_spawn_dict,
            'fire_spawn': fire_spawn_dict,
            'ice_healing_area': ice_healing_area_dict,
            'fire_healing_area': fire_healing_area_dict
        }

    def create_new_game_state_model(self, current_game_state, serialized_data, simulation_id):
        return GameStateModel(
            username=current_game_state.username,
            team=current_game_state.team.value,
            mode=current_game_state.mode.value,
            board=json.dumps(serialized_data['board']),
            ice_spawn=json.dumps(serialized_data['ice_spawn']),
            fire_spawn=json.dumps(serialized_data['fire_spawn']),
            ice_healing_area=json.dumps(serialized_data['ice_healing_area']),
            fire_healing_area=json.dumps(serialized_data['fire_healing_area']),
            timestamp=datetime.utcnow(),
            simulation_id=simulation_id
        )
api.add_resource(UpdateStateResource, '/update_state')

