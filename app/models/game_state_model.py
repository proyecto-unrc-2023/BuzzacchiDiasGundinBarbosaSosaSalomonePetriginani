
from api import db
from sqlalchemy import Enum
from logic.game_state import Team, GameMode

class GameStateModel(db.Model):
    __tablename__ = 'game_states'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    # team = db.Column(Enum(Team.IceTeam, Team.FireTeam))
    # mode = db.Column(Enum(GameMode.NOT_STARTED, GameMode.SPAWN_PLACEMENT, GameMode.SIMULATION, GameMode.FINISHED), nullable=False)
    team = db.Column(db.String)
    mode = db.Column(db.String)
    board = db.Column(db.Text)
    ice_spawn = db.Column(db.Text)
    fire_spawn = db.Column(db.Text)
    ice_healing_area = db.Column(db.Text)
    fire_healing_area = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'team': self.team,
            'mode': self.mode,
            'fire_spawn': self.fire_spawn,
            'ice_spawn': self.ice_spawn,
            'ice_healing_area': self.ice_healing_area,
            'fire_healing_area': self.fire_healing_area,
            'board': self.board
        }