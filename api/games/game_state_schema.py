from marshmallow import Schema, fields
from api.games.board_schema import BoardSchema
from marshmallow_enum import EnumField
from logic.game_state import Team

class GameStateSchema(Schema):
    board = fields.nested(BoardSchema())
    username = fields.Str()
    team = EnumField(Team, by_value=True)
    