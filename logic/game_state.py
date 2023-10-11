from enum import Enum


from logic.board import Board
from logic.spawn import Spawn, IceSpawn, FireSpawn

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
        self.columns = None
        self.rows = None
        self.user_team = None
        self.username = None

    def new_game(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = Board(rows, columns)
        self.mode = GameMode.SPAWN_PLACEMENT

    def half_game(self):
        self.mode = GameMode.SPAWN_PLACEMENT

    def add_spawn(self, rows, columns):
        if (self.user_team == "IceTeam"):
            spawn = IceSpawn((rows, columns), self.board)
        else:
            spawn = FireSpawn((rows, columns), self.board)
        self.board.add_spawn(rows, columns, spawn)
        self.mode = GameMode.SIMULATION
    
    def set_username(self, username):
        self.username = username

    def set_team(self, team):
        self.team = team
        

    def get_mode(self):
        return self.mode
    
    def get_board(self):
        return self.board