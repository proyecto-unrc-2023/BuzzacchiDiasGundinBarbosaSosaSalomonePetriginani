from flask import Blueprint
from flask_restful import Api

simulation_bp = Blueprint('simulation', __name__)

# wrap the blueprint with the Api object
api = Api(simulation_bp)

# Import module routes
from api.routes import routes_for_testing
from api.routes import set_spawn
from app.schemas.board_schema import BoardSchema
from app.models.board_model import BoardModel
from app.schemas.game_state_schema import GameStateSchema
from app.models.game_state_model import GameStateModel