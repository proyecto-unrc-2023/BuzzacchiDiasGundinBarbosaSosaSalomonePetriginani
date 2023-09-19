from flask import Flask, render_template, request, redirect, url_for
from logic.game_state import GameState

app = Flask(__name__, static_folder='static')

# Display route page
@app.route("/")
def home():
    return render_template('index.html')

# Route for select team
@app.route("/start_game", methods=['GET', 'POST'])
def select_team():
    if request.method == 'POST':
        username = request.form['username']
        team = request.form['team']
        game = GameState()
        game.new_game(50, 50, username, team)
        return redirect(url_for('game', username=username, team=team))
    return redirect(url_for('home'))

# Route for displaying the game
@app.route("/game/<username>/<team>")
def game(username, team):
    return render_template('game.html', username=username, team=team)
