
from api import db

class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    user_team = db.Column(db.String)
    game_mode = db.Column(db.String, nullable=False)
    board = db.Column(db.Text)
