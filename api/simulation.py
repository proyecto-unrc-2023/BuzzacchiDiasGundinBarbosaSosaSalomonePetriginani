from flask import request, jsonify
from app.schemas.cell_schema import CellSchema
from app.schemas.board_schema import BoardSchema
from logic.cell import Level, IceCell, FireCell
from logic.board import Board
from api.routes import simulation_bp
from random import randint, choice
from logic.spawn import IceSpawn
from app.schemas.game_state_schema import GameStateSchema
from app.models.game_state_model import GameStateModel
from logic.game_state import GameMode, Team
# from app.schemas.spawn_schema import SpawnSchema
# from app.schemas.healing_area_schema import HealingAreaSchema
from logic.game_controller import GameController
from api import db
import json

# Route to start the game and receive data 
@simulation_bp.route('/start', methods=['POST'])
def start():
    if request.method == 'POST':
        data = request.json  

        selected_username = data.get('username')
        selected_team = data.get('team')

        game_controller = GameController()
        game_controller.new_game(10, 10)
        game_controller.set_username(selected_username)
        game_controller.set_team(selected_team)

        board_schema = BoardSchema()

        #Logic to add to DB actual game state
        game_state_data = {
            'username': game_controller.get_username(),
            'team': game_controller.get_team(),
            'mode': game_controller.get_mode(),
            'board': board_schema.dump(game_controller.get_board())
        }
        
        # Load the game state data into the schema
        game_state_schema = GameStateSchema()

        serialized_game_state_data = game_state_schema.load(game_state_data)

        game_state_model_instance= GameStateModel(
            username=serialized_game_state_data['username'],
            team=serialized_game_state_data['team'].value,
            mode=serialized_game_state_data['mode'].value,
            # team=Team(serialized_game_state_data['team']),
            # mode=GameMode(serialized_game_state_data['mode']),
            board=json.dumps(serialized_game_state_data['board'])
        )

        db.session.add(game_state_model_instance)
        db.session.commit()

        return jsonify({'game_state': game_state_model_instance.to_dict()}), 200








######Tests routes
# Route to start the game and receive data (POST)
# @simulation_bp.route('/start', methods=['POST'])
# def start():
#     if request.method == 'POST':
#         data = request.json  # Receive data in JSON format from the request

#         # Extract data from the JSON form
#         username = data.get('username')
#         team = data.get('team')

#         # Save the data in the global variable
#         game_data['username'] = username
#         game_data['team'] = team

#         game = GameState()
#         game.new_game(50, 50, username, team)

#         response_data = {
#             'message': 'Received data',
#             'username': username,
#             'team': team
#         }
#         return jsonify(response_data), 200

# Obtain game data
# @simulation_bp.route('/get_game_data', methods=['GET'])
# def get_game_data():
#     return jsonify(game_data)




# ###Routes for testing
# @simulation_bp.route('/get_cells', methods=['GET'])
# def get_cells():
#     cell = FireCell(level=Level.LEVEL_1, life=20, position=(0, 0))
#     cell_schema = CellSchema()
#     cell_json = cell_schema.dump(cell)
#     return jsonify(cell_json)  



# @simulation_bp.route('/get_board', methods=['GET'])
# def get_board():
#     board = Board(5, 5)

#     board.create_spawn(1,1, IceSpawn)

#     # crear celulas
#     for _ in range(1):
#         level = Level.LEVEL_1
#         life = randint(1, 20)
#         position = (randint(0, 1), randint(0, 1))
#         cell_type = choice([IceCell, FireCell])
#         cell = cell_type(level=level, life=life, position=position)
#         board.add_cell(*position, cell)

#     # Serializar el tablero a JSON usando BoardSchema
#     board_schema = BoardSchema()
#     board_json = board_schema.dump(board)

#     # Devolver el tablero serializado
#     return jsonify(board_json)


