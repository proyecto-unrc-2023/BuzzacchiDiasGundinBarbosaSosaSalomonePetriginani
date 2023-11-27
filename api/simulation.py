from flask import request, jsonify, session
from api.routes import simulation_bp
from app.schemas.game_state_schema import GameStateSchema
from app.models.game_state_model import GameStateModel
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

# This route is used to setup an username and team in a game state
# It expects a POST request with a JSON body containing 'username' and 'team'
@simulation_bp.route('/start', methods=['POST'])
def start():
    try:
        validate_start_request(request.json)

        selected_username = request.json.get('username')
        selected_team = request.json.get('team')

        game_controller = create_game_controller(selected_username, selected_team)

        game_state_model_instance = save_game_state_to_db(game_controller)

        session['username'] = selected_username
        session['id'] = game_state_model_instance.id

        return jsonify({'game_state': game_state_model_instance.to_dict()}), 200

    except ValueError as e:
        return jsonify({'message': str(e)}), 400

# This function validates the request data for the 'start' endpoint.
def validate_start_request(data):
    selected_username = data.get('username')
    selected_team = data.get('team')

    if not isinstance(selected_username, str) or not selected_username.strip():
        raise ValueError('Username must be a non-empty string')

    if selected_team not in ('IceTeam', 'FireTeam'):
        raise ValueError('Team must be either "IceTeam" or "FireTeam"')

# This function creates a new GameController with the provided username and team.
def create_game_controller(username, team):
    game_controller = GameController()
    game_controller.set_username(username)
    game_controller.set_team(team)
    return game_controller

# This function saves the current game state to the database.
def save_game_state_to_db(game_controller):
    game_state_data = {
        'username': game_controller.get_username(),
        'team': game_controller.get_team(),
        'mode': game_controller.get_mode(),
    }

    game_state_schema = GameStateSchema()
    serialized_game_state_data = game_state_schema.load(game_state_data)

    game_state_model_instance = GameStateModel(
        username=serialized_game_state_data['username'],
        team=serialized_game_state_data['team'].value,
        mode=serialized_game_state_data['mode'].value,
    )

    db.session.add(game_state_model_instance)
    db.session.commit()

    return game_state_model_instance

# This endpoint retrieves and returns the username and team of the authenticated user from a game session.
@simulation_bp.route('/get_username_and_team', methods=['GET'])
def get_username_and_team():
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

# This endpoint retrieves and returns the winner team if a spawn has died.
@simulation_bp.route('/get_winner_team', methods=['GET'])
def get_winner_team():
    game_id = session.get('id')
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

@simulation_bp.route('/get_winner_team_by_id/<int:game_state_id>', methods=['GET'])
def get_winner_team_by_id(game_state_id):
    game_state = GameStateModel.query.filter_by(id=game_state_id).first()
    if game_state:
        game_state_dict = game_state.to_dict()
        
        ice_spawn_json = json.loads(game_state_dict.get('ice_spawn'))  
        if ice_spawn_json:
            ice_spawn_life = ice_spawn_json.get('life')
            if ice_spawn_life > 0:
                return jsonify({'winner_team': 'IceTeam'})
            else:
                return jsonify({'winner_team': 'FireTeam'})

    return {'error': 'No game state found'}, 404





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


