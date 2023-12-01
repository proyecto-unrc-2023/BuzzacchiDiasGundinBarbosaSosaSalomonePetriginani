
from api import db
from datetime import datetime
import uuid
class GameStateModel(db.Model):
    __tablename__ = 'game_states'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    team = db.Column(db.String)
    mode = db.Column(db.String)
    board = db.Column(db.Text)
    ice_spawn = db.Column(db.Text)
    fire_spawn = db.Column(db.Text)
    ice_healing_area = db.Column(db.Text)
    fire_healing_area = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    simulation_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), nullable=False)

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
            'board': self.board,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'simulation_id': self.simulation_id  
        }