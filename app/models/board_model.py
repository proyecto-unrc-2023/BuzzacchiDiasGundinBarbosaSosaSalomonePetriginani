
from api import db

class BoardModel(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    rows = db.Column(db.Integer, nullable=False)
    columns = db.Column(db.Integer, nullable=False)
    board = db.Column(db.Text)



