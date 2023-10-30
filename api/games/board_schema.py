from marshmallow import Schema, fields

from api.games.box_schema import BoxSchema

class BoardSchema(Schema):
    rows = fields.Int()
    columns = fields.Int()
    board = fields.List(fields.List(fields.Nested(BoxSchema)))
   