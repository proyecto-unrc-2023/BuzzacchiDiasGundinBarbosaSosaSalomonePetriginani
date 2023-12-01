from flask import Blueprint
from flask_restful import Api

simulation_bp = Blueprint('simulation', __name__)

# wrap the blueprint with the Api object
api = Api(simulation_bp)

# Import module routes
from api.routes import new_game
from api.routes import update_state
from api.routes import google_sign_in
from api.routes import simulation_history
from api.routes import simulation_replay

