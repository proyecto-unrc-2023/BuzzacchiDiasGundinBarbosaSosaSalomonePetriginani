from flask import jsonify, request, session
from flask_restful import Resource
from api.routes import api
from sqlalchemy import func
from app.models.game_state_model import GameStateModel
from api import db

class SimulationHistoryResource(Resource):
    def post(self):
        username = request.json['username']

        simulations = db.session.query(
            GameStateModel.simulation_id,
            func.min(GameStateModel.timestamp).label('start_time'),
            GameStateModel.team
        ).filter_by(
            username=username,
                mode='SIMULATION'  
        ).group_by(
            GameStateModel.simulation_id,
        ).all()

        result = [{"simulation_id": sim_id, "start_time": start_time.isoformat() if start_time else None, "team": team} for sim_id, start_time, team in simulations]
        return result





api.add_resource(SimulationHistoryResource, '/simulation_history')
