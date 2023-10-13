from marshmallow import Schema, fields #, post_load
from logic.cell import Level
from marshmallow_enum import EnumField

class SpawnSchema(Schema):
    life = fields.Int()
    positions = fields.List(fields.Tuple((fields.Int(), fields.Int())))
    type = fields.Str()