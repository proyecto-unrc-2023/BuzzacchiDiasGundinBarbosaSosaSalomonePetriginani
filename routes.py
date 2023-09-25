from flask import Flask, request, jsonify
from logic.game_state import GameState

app = Flask(__name__)

# Global variable to store game data
game_data = {
    'username': None,
    'team': None,
}

# Route to start the game and receive data (POST)
@app.route('/start_game', methods=['POST'])
def start_game():
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
@app.route('/get_game_data', methods=['GET'])
def get_game_data():
    return jsonify(game_data)




if __name__ == '__main__':
    app.run(debug=True)

