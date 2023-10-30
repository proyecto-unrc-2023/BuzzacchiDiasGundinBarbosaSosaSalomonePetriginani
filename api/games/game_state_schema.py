from marshmallow import Schema, fields
from api.games.board_schema import BoardSchema
from marshmallow_enum import EnumField
from logic.game_state import Team, GameMode
from api.games.spawn_schema import SpawnSchema
from api.games.healing_area_schema import HealingAreaSchema

class GameStateSchema(Schema):
    board = fields.Nested(BoardSchema, allow_none=True)
    username = fields.Str(allow_none=True)
    team = EnumField(Team, by_value=True, allow_none=True)
    mode = EnumField(GameMode, by_value=True, allow_none=True)
    ice_spawn = fields.Nested(SpawnSchema, allow_none=True)
    fire_spawn = fields.Nested(SpawnSchema, allow_none=True)
    ice_healing_area = fields.Nested(HealingAreaSchema, allow_none=True)
    fire_healing_area = fields.Nested(HealingAreaSchema, allow_none=True)