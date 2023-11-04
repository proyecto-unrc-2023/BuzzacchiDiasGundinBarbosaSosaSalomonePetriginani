from marshmallow import fields, Schema, post_load
from app.schemas.cell_schema import CellSchema
from app.schemas.healing_area_schema import HealingAreaSchema
from app.schemas.spawn_schema import SpawnSchema
from logic.box import Box

class BoxSchema(Schema):
    spawn = fields.Nested(SpawnSchema, allow_none=True)
    fire_cells = fields.List(fields.Nested(CellSchema), allow_none=True)
    ice_cells = fields.List(fields.Nested(CellSchema), allow_none=True)
    fire_healing_area = fields.Nested(HealingAreaSchema, allow_none=True)
    ice_healing_area = fields.Nested(HealingAreaSchema, allow_none=True)
    pos = fields.Tuple((fields.Int(), fields.Int()))

    # @post_load
    # def make_box(self, data, **kwargs):
    #     return Box(**data)