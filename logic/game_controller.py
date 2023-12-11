from logic.board import Board
from logic.cell import Cell, Level, FireCell, IceCell
from logic.spawn import Spawn, IceSpawn, FireSpawn
from logic.game_state import GameMode, Team, GameState
from app.schemas.game_state_schema import GameStateSchema
from app.models.game_state_model import GameStateModel
from flask import jsonify


class GameController:
    
    def __init__(self, game_state=None):
        if game_state is not None:
            self.game_state = game_state
        else:
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
    
    def get_game_state(self):
        return self.game_state
    
    def get_username(self):
        return self.game_state.get_username()
    
    def no_spawns_in_pos(self, row, column):
        return self.game_state.no_spawns_in_pos(row, column)
    
    def add_spawn(self, positions):
        self.game_state.add_spawn(positions)
        
    def create_spawn(self, row, column, spawn_type):
        if eval(spawn_type) == IceSpawn:
            self.game_state.create_spawn(row, column, IceSpawn)
        else:
            self.game_state.create_spawn(row, column, FireSpawn)

    def create_cell(self, row, column, cell_type, level, life):
        if eval(cell_type) == IceCell:
            self.game_state.create_cell(row, column, IceCell, level, life)
        else:
            self.game_state.create_cell(row, column, FireCell, level, life)

    def create_healing_area(self, row, column, affected_cell_type):
        if eval(affected_cell_type) == IceCell:
            self.game_state.create_healing_area(row, column, IceCell)
        else:
            self.game_state.create_healing_area(row, column, FireCell)

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
    
    # only for behave healing
    def get_positions_healing(self, team):
        if(team == IceCell):
            return self.game_state.ice_healing_area.get_positions()
        else:
            return self.game_state.fire_healing_area.get_positions()
    
    def apply_healing(self):
        self.game_state.apply_healing()
    
    def get_adjacents_for_move(self, row, column, team):
        pos = (row, column)
        return self.game_state.get_adjacents_for_move(pos, team)
    
    def get_ice_spawn(self):
        return self.game_state.get_ice_spawn()
    
    def get_fire_spawn(self):
        return self.game_state.get_fire_spawn()
    
    def get_ice_healing_area(self):
        return self.game_state.get_ice_healing_area()
    
    def get_fire_healing_area(self):
        return self.game_state.get_fire_healing_area()
    
    def get_cells_in_spawn(self, spawn):
        return self.game_state.get_cells_in_spawn(spawn)

    def find_matching_cells(self, position, cell_type, life_points, level):
        cells = self.get_cells(*position)
        matching_cells = [cell for cell in cells if isinstance(cell, eval(cell_type)) and cell.get_life() == life_points and cell.get_level() == Level(level)]
        return matching_cells

    def update_state(self):
        self.game_state.update_state()

    def serialize_game_state(self, game_state):
        game_state_schema = GameStateSchema()
        serialize_game_state = game_state_schema.dump(game_state)
        return jsonify(serialize_game_state)
    
    def generate_cells(self):
        self.game_state.generate_cells()
