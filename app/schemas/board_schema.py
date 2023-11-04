from marshmallow import Schema, fields, post_load
from logic.board import Board
from app.schemas.box_schema import BoxSchema

class BoardSchema(Schema):
    rows = fields.Int()
    columns = fields.Int()
    board = fields.List(fields.List(fields.Nested(BoxSchema)))
   
    # @post_load
    # def make_object(self, data, **kwargs):
    #     return Board(**data)