from logic.board import Board
from logic.cell import Cell, Level, FireCell, IceCell
from logic.spawn import Spawn, IceSpawn, FireSpawn
from logic.game_state import GameMode, Team, GameState

class GameController:
    
    def __init__(self):
        self.game_state = GameState()
        
    def create_user(self, user_name):
        self.game_state.set_username(user_name)
        
    def choice_team(self, team):
        self.game_state.set_team(team)
        
    def new_game(self):
        self.game_state.new_game(50,50)
    
    def new_game(self, row, column):
        self.game_state.new_game(row, column)
        
    def get_state_mode(self):
        return self.game_state.get_mode()
    
    def spawn_placement(self, pos):
        self.game_state.add_spawn(pos[0], pos[1])
        
    def add_cell_in_pos:
        