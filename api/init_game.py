from flask import request, jsonify, Blueprint
from logic.game_state import GameState
from api.games.cell_schema import CellSchema
from api.games.board_schema import BoardSchema
from logic.cell import Cell, Level, IceCell, FireCell
from logic.board import Board
from api.games import init_game_bp
from random import randint, choice
from logic.spawn import IceSpawn

# Global variable to store game data
game_data = {
    'username': None,
    'team': None,
}

# Route to start the game and receive data (POST)
@init_game_bp.route('/start', methods=['POST'])
def start():
    if request.method == 'POST':
        data = request.json  # Receive data in JSON format from the request

        # Extract data from the JSON form
        username = data.get('username')
        team = data.get('team')

        # Save the data in the global variable
        game_data['username'] = username
        game_data['team'] = team

        game = GameState()
        game.new_game(50, 50, username, team)

        response_data = {
            'message': 'Received data',
            'username': username,
            'team': team
        }
        return jsonify(response_data), 200

# Obtain game data
@init_game_bp.route('/get_game_data', methods=['GET'])
def get_game_data():
    return jsonify(game_data)




###Routes for testing
@init_game_bp.route('/get_cells', methods=['GET'])
def get_cells():
    cell = FireCell(level=Level.LEVEL_1, life=20, position=(0, 0))
    cell_schema = CellSchema()
    cell_json = cell_schema.dump(cell)
    return jsonify(cell_json)  



@init_game_bp.route('/get_board', methods=['GET'])
def get_board():
    board = Board(2, 2)

    # ice_spawn = IceSpawn(300, [(0,0),(1,0),(0,1),(1,1)], board=Board)
    # board.add_spawn(ice_spawn.positions, ice_spawn)

    # crear celulas
    for _ in range(1):
        level = Level.LEVEL_1
        life = randint(1, 20)
        position = (randint(0, 1), randint(0, 1))
        cell_type = choice([IceCell, FireCell])
        cell = cell_type(level=level, life=life, position=position)
        board.add_cell(*position, cell)

    # Serializar el tablero a JSON usando BoardSchema
    board_schema = BoardSchema()
    board_json = board_schema.dump(board)

    # Devolver el tablero serializado
    return jsonify(board_json)


