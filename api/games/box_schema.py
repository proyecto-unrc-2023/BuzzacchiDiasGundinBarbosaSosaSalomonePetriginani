from marshmallow import fields, Schema
from api.games.cell_schema import CellSchema
from api.games.healing_area_schema import HealingAreaSchema
from api.games.spawn_schema import SpawnSchema

class BoxSchema(Schema):
    spawn = fields.Nested(SpawnSchema, allow_none=True)
    fire_cells = fields.List(fields.Nested(CellSchema))
    ice_cells = fields.List(fields.Nested(CellSchema))
    fire_healing_area = fields.Nested(HealingAreaSchema, allow_none=True)
    ice_healing_area = fields.Nested(HealingAreaSchema, allow_none=True)
    pos = fields.Tuple((fields.Int(), fields.Int()))