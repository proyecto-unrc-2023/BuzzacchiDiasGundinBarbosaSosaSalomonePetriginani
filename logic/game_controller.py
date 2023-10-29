from logic.board import Board
from logic.cell import Cell, Level, FireCell, IceCell
from logic.spawn import Spawn, IceSpawn, FireSpawn
from logic.game_state import GameMode, Team, GameState

class GameController:
    
    def __init__(self):
        self.game_state = GameState()
        
    def set_username(self, user_name):
        self.game_state.set_username(user_name)
        
    def set_team(self, team):
        self.game_state.set_team(team)
        
    # def new_game(self):
    #     self.game_state.new_game(50,50)
    
    def new_game(self, rows, columns):
        self.game_state.new_game(rows, columns)

    def half_game(self):
        self.game_state.half_game()
        
    def get_mode(self):
        return self.game_state.get_mode()
    
    def get_board(self):
        return self.game_state.get_board()
    
    def get_team(self):
        return self.game_state.get_team()
    
    def get_spawn(self, spawn_type):
        return self.game_state.get_spawn(spawn_type)
    
    def no_spawns_in_pos(self, row, column):
        return self.game_state.no_spawns_in_pos(row, column)
    
    #Corregir
    def add_spawn(self, positions):
        self.game_state.add_spawn(positions)
        
    def create_spawn(self, row, column, spawn_type):
        if eval(spawn_type) == IceSpawn:
            self.game_state.create_spawn(row, column, IceSpawn)
        else:
            self.game_state.create_spawn(row, column, FireSpawn)

    def create_cell(self, row, column, cell_type, level, life):
        if eval(cell_type) == IceCell:
            self.game_state.create_cell(row, column, cell_type, level, life)
        else:
            self.game_state.create_cell(row, column, cell_type, level, life)

    def execute_fights(self):
        self.game_state.execute_fights_in_all_positions()
        
    def execute_movement(self):
        self.game_state.execute_movements_in_all_positions()
        
    def execute_fusion(self):
        self.game_state.execute_fusions_in_all_positions()

    def get_cells(self, row, column):
        return self.game_state.get_cells(row, column)
    
    def get_ice_cells(self, row, column):
        return self.game_state.get_ice_cells(row, column)
    
    def get_fire_cells(self, row, column):
        return self.game_state.get_fire_cells(row, column)
    
    def get_adyacents_pos(self, row, column):
        pos = (row, column)
        return self.game_state.get_adjacents_pos(pos)
    
    def get_adjacents_for_move(self, row, column, team):
        pos = (row, column)
        return self.game_state.get_adjacents_for_move(pos, team)
    
    def get_ice_spawn(self):
        return self.game_state.get_ice_spawn()
    
    def get_cells_in_spawn(self, spawn):
        return self.game_state.get_cells_in_spawn(spawn)


    def find_matching_cells(self, position, cell_type, life_points, level):
        cells = self.get_cells(*position)
        matching_cells = [cell for cell in cells if isinstance(cell, eval(cell_type)) and cell.get_life() == life_points and cell.get_level() == level]
        return matching_cells

    
    def generate_cell(self):
        self.game_state.generate_cell()
