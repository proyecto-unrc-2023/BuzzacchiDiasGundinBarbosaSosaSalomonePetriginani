from enum import Enum

from logic.board import Board


class GameMode(Enum):
    NOT_STARTED = 1
    SPAWN_PLACEMENT = 2
    SIMULATION = 3

class GameState:

    def __init__(self):
        self.mode = GameMode.NOT_STARTED
        self.board = None
        self.columns = None
        self.rows = None

    def new_game(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = Board(rows, columns)
        self.mode = GameMode.SPAWN_PLACEMENT

