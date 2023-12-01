from flask import request
from flask_restful import Resource
from api.routes import api
from sqlalchemy import func
from app.models.game_state_model import GameStateModel
from api import db
from pytz import timezone

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

        finished_simulations = db.session.query(
            GameStateModel.simulation_id
        ).filter_by(
            username=username,
            mode='FINISHED'
        ).all()
        
        finished_simulations_ids = [sim_id for sim_id, in finished_simulations]

        result = []
        for sim_id, start_time, team in simulations:
            # Convert start_time to the client's timezone
            start_time = start_time.replace(tzinfo=timezone('UTC'))
            start_time = start_time.astimezone(timezone('America/Argentina/Buenos_Aires'))

            status = "Finished" if sim_id in finished_simulations_ids else "Not Finished"
            result.append({"simulation_id": sim_id, "start_time": start_time.isoformat(), "team": team, "status": status})

        return result





api.add_resource(SimulationHistoryResource, '/simulation_history')
