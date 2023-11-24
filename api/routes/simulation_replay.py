from flask import request
from sqlalchemy import and_
from flask_restful import Resource
from app.models.game_state_model import GameStateModel
from api import db
from api.routes import api
from datetime import datetime

class SimulationReplayResource(Resource):
    def post(self):
        simulation_id = request.json['simulation_id']
        timestamp_str = request.json.get('last_timestamp')

        if timestamp_str is not None:
            # Convert from text to datetime python object
            timestamp = datetime.fromisoformat(timestamp_str)

            game_state = GameStateModel.query.filter(
                and_(
                    GameStateModel.simulation_id == simulation_id,
                    GameStateModel.timestamp > timestamp
                )
            ).order_by(GameStateModel.timestamp).first()
        else:
            game_state = GameStateModel.query.filter_by(
                simulation_id=simulation_id
            ).order_by(GameStateModel.timestamp).first()

        if game_state:
            return {'game_state': game_state.to_dict(), 'last_timestamp': game_state.timestamp.isoformat()}

        return {'error': 'No game state found'}, 404


api.add_resource(SimulationReplayResource, '/simulation_replay')
