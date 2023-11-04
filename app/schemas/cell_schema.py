from marshmallow import Schema, fields, post_load
from logic.cell import Level
from marshmallow_enum import EnumField
from logic.cell import Cell

class CellSchema(Schema):
    level = EnumField(Level, by_value=True)
    life = fields.Int()
    position = fields.Tuple((fields.Int(), fields.Int()))

    # @post_load
    # def make_cell(self, data, **kwargs):
    #     return Cell(**data)

