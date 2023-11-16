from flask import request, jsonify, session
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

def get_authenticated_user():
    username = session.get('username')
    if username:
        game_state = GameStateModel.query.filter_by(id=session['id']).first()
        if game_state:
            return game_state.to_dict()['username']

    return None

# Route to start the game and receive data 
@simulation_bp.route('/start', methods=['POST'])
def start():
    if request.method == 'POST':
        data = request.json  

        selected_username = data.get('username')
        # Check username
        if not isinstance(selected_username, str) or not selected_username.strip():
            return {'message': 'Username must be a non-empty string'}, 400
        
        selected_team = data.get('team')
        # Check team
        if selected_team not in ('IceTeam', 'FireTeam'):
            return {'message': 'Team must be either "IceTeam" or "FireTeam"'}, 400
        
        game_controller = GameController()
        game_controller.set_username(selected_username)
        game_controller.set_team(selected_team)

        #Logic to add to DB actual game state
        game_state_data = {
            'username': game_controller.get_username(),
            'team': game_controller.get_team(),
            'mode': game_controller.get_mode(),
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
            #board=json.dumps(serialized_game_state_data['board'])
        )

        db.session.add(game_state_model_instance)
        db.session.commit()
        session['username'] = selected_username
        session['id'] = game_state_model_instance.id
        return jsonify({'game_state': game_state_model_instance.to_dict()}), 200


@simulation_bp.route('/get_username_and_team', methods=['GET'])
def get_username_and_team():
    if request.method == 'GET':
        auth_user = get_authenticated_user()
        
        if auth_user:
            game_state = GameStateModel.query.filter_by(id=session['id']).first()

            if game_state:
                game_state_dict = game_state.to_dict()
                username = game_state_dict['username']
                team = game_state_dict['team']
                return jsonify({'username': username, 'team': team}), 200
            else:
                return {'message': 'Game state not found for the authenticated user'}, 404
        else:
            return {'message': 'Unauthenticated user'}, 401

@simulation_bp.route('/get_winner_team', methods=['GET'])
def get_winner_team():
    if request.method == 'GET':

        game_id = session['id']
        game_state = GameStateModel.query.filter_by(id=game_id).first()
        if game_state:
            game_state_dict = game_state.to_dict()

            ice_spawn_json = json.loads(game_state_dict.get('ice_spawn'))  
            if ice_spawn_json:
                ice_spawn_life = ice_spawn_json.get('life')
                if ice_spawn_life > 0:
                    return jsonify({'winner_team': 'IceTeam'})
                else:
                    return jsonify({'winner_team': 'FireTeam'})








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


