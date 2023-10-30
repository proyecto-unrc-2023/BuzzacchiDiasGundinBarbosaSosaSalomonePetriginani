
from marshmallow import Schema, fields 

class SpawnSchema(Schema):
    life = fields.Int()
    positions = fields.List(fields.Tuple((fields.Int(), fields.Int())))
    type = fields.Str()