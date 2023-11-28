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
from datetime import datetime
from sqlalchemy import desc


class UpdateStateResource(Resource):
    def get(self):
        game_state_model = GameStateModel.query.filter_by(simulation_id=session['simulation_id']).order_by(desc(GameStateModel.timestamp)).first()
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

        # Crear una nueva instancia de GameStateModel con los valores actualizados
        new_game_state_model = GameStateModel(
            username=current_game_state.username,
            team=current_game_state.team.value,
            mode=current_game_state.mode.value,
            board=json.dumps(board_dict),
            ice_spawn=json.dumps(ice_spawn_dict),
            fire_spawn=json.dumps(fire_spawn_dict),
            ice_healing_area=json.dumps(ice_healing_area_dict),
            fire_healing_area=json.dumps(fire_healing_area_dict),
            timestamp=datetime.utcnow(),
            simulation_id=game_state_data_model.get('simulation_id')
        )

        # Agregar la nueva instancia a la sesión de la base de datos
        db.session.add(new_game_state_model)

        # Convertir la instancia de GameStateModel a un diccionario para ver el estado del juego actualizado en la respuesta
        game_state_dict = new_game_state_model.to_dict()

        db.session.commit()
        return {'updated_game_state': game_state_dict, 'board_str': current_board_str}, 200
    
    def post(self):
        data = request.json
        game_state_model = GameStateModel.query.filter_by(simulation_id=data['simulation_id']).order_by(desc(GameStateModel.timestamp)).first()
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

        # Crear una nueva instancia de GameStateModel con los valores actualizados
        new_game_state_model = GameStateModel(
            username=current_game_state.username,
            team=current_game_state.team.value,
            mode=current_game_state.mode.value,
            board=json.dumps(board_dict),
            ice_spawn=json.dumps(ice_spawn_dict),
            fire_spawn=json.dumps(fire_spawn_dict),
            ice_healing_area=json.dumps(ice_healing_area_dict),
            fire_healing_area=json.dumps(fire_healing_area_dict),
            timestamp=datetime.utcnow(),
            simulation_id=game_state_data_model.get('simulation_id')
        )
        session['id'] = game_state_data_model.get('id')
        # Agregar la nueva instancia a la sesión de la base de datos
        db.session.add(new_game_state_model)

        # Convertir la instancia de GameStateModel a un diccionario para ver el estado del juego actualizado en la respuesta
        game_state_dict = new_game_state_model.to_dict()

        db.session.commit()
        return {'updated_game_state': game_state_dict, 'board_str': current_board_str}, 200
api.add_resource(UpdateStateResource, '/update_state')

