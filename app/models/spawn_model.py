
from api import db

class SpawnModel(db.Model):
    __tablename__ = 'spawns'
    id = db.Column(db.Integer, primary_key=True)
    life = db.Column(db.Integer, nullable=False)
    positions = db.Column(db.Text)  
    type = db.Column(db.String(80), nullable=False)