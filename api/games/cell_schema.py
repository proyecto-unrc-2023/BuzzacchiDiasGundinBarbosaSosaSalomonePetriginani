from marshmallow import Schema, fields 
from logic.cell import Level
from marshmallow_enum import EnumField

class CellSchema(Schema):
    level = EnumField(Level, by_value=True)
    life = fields.Int()
    position = fields.Tuple((fields.Int(), fields.Int()))
    type = fields.Str()



