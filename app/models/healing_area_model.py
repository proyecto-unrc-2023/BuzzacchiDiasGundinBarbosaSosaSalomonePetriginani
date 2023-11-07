
from api import db

class HealingAreaModel(db.Model):
    __tablename__ = 'healing_areas'
    id = db.Column(db.Integer, primary_key=True)
    positions = db.Column(db.Text)  
    duration = db.Column(db.Integer, nullable=False)
    healing_rate = db.Column(db.Integer, nullable=False)
    affected_cell_type = db.Column(db.Text)  

