
from marshmallow import Schema, fields, pre_dump
from logic.healing_area import HealingArea

class HealingAreaSchema(Schema):
    positions = fields.List(fields.Tuple((fields.Int(), fields.Int())))
    duration = fields.Int()
    healing_rate = fields.Int()
    affected_cell_type = fields.Str()

    # @pre_dump
    # def convert_affected_cell_type_to_string(self, obj, **kwargs):
    #     if isinstance(obj.affected_cell_type, type):
    #         # Si es un objeto de tipo, toma su nombre como string
    #         obj.affected_cell_type = obj.affected_cell_type.__name__
    #     return obj