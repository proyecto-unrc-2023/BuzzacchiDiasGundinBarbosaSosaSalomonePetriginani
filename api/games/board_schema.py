from marshmallow import Schema, fields
from api.games.cell_schema import CellSchema
from api.games.spawn_schema import SpawnSchema
from logic.cell import IceCell, FireCell
from logic.spawn import IceSpawn, FireSpawn
from marshmallow_oneofschema import OneOfSchema

class CellOrSpawnSchema(OneOfSchema):
    type_schemas = {
        "IceCell": CellSchema,
        "FireCell": CellSchema,
        "IceSpawn": SpawnSchema,
        "FireSpawn": SpawnSchema
    }

    def get_obj_type(self, obj):
        if isinstance(obj, IceCell):
            return "IceCell"
        elif isinstance(obj, FireCell):
            return "FireCell"
        elif isinstance(obj, IceSpawn):
            return "IceSpawn"
        elif isinstance(obj, FireSpawn):
            return "FireSpawn"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))

class BoardSchema(Schema):
    rows = fields.Int()
    columns = fields.Int()
    board = fields.List(fields.List(fields.List(fields.Nested(CellOrSpawnSchema))))
   