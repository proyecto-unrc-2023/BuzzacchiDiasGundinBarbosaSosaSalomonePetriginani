from enum import Enum
from logic.board import Board
from logic.spawn import IceSpawn, FireSpawn

class GameMode(Enum):
    NOT_STARTED = 1
    SPAWN_PLACEMENT = 2
    SIMULATION = 3

class Team(Enum):
    IceTeam = "IceTeam"
    FireTeam = "FireTeam"

class GameState:

    def __init__(self):
        self.mode = GameMode.NOT_STARTED
        self.board = None
        self.user_team = None
        self.username = None
        self.ice_spawn = None
        self.fire_spawn = None

    def new_game(self, rows, columns, username = None, team = None):
        self.rows = rows
        self.columns = columns
        self.board = Board(rows, columns)
        self.mode = GameMode.SPAWN_PLACEMENT
        self.username = username
        self.team = team

    def half_game(self):
        self.mode = GameMode.SPAWN_PLACEMENT

    def add_spawn(self, rows, columns, IceSpawn=None, FireSpawn=None):
        if self.team == Team.IceTeam:
            self.board.add_spawn(rows, columns, IceSpawn)
        else:
            self.board.add_spawn(rows, columns, FireSpawn)
        self.mode = GameMode.SIMULATION
    
    def set_username(self, username):
        self.username = username

    def set_team(self, team):
        self.team = team

    def get_mode(self):
        return self.mode
    
    def get_board(self):
        return self.board