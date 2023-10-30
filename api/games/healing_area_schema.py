
from marshmallow import Schema, fields

class HealingAreaSchema(Schema):
    positions = fields.List(fields.Tuple((fields.Int(), fields.Int())))
    duration = fields.Int()
    healing_rate = fields.Int()
    #type = fields.Str()