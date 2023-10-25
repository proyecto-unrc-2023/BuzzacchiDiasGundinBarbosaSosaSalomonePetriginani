from flask import Blueprint
from flask_restful import Api

init_game_bp = Blueprint('init_game', __name__)

# wrap the blueprint with the Api object
api = Api(init_game_bp)

# Import module routes
from api.games import routes
from api.games import board_schema
from api.games import board_model