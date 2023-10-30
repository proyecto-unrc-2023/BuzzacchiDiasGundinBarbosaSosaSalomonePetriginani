
from api import db
from enum import Enum
from logic.game_state import Team, GameMode

class GameStateModel(db.Model):
    __tablename__ = 'game_states'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    team = db.Column(db.Enum(Team))
    mode = db.Column(db.Enum(GameMode), nullable=False)
    board = db.Column(db.Text)
    ice_spawn = db.Column(db.Text)
    fire_spawn = db.Column(db.Text)
    ice_healing_area = db.Column(db.Text)
    fire_healing_area = db.Column(db.Text)
