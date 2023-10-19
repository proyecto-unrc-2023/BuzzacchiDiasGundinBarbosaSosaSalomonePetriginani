from enum import Enum
import random

from logic.cell import IceCell, FireCell, Level
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
        self.team = None
        self.username = None
        self.ice_spawn = None
        self.fire_spawn = None
        #self.cell_id_counter = 1

    def new_game(self, rows, columns):
        self.board = Board(rows, columns)
        self.mode = GameMode.SPAWN_PLACEMENT

    def half_game(self):
        self.mode = GameMode.SPAWN_PLACEMENT

    def set_username(self, username):
        self.username = username

    def set_team(self, team):
        self.team = team
   
    def create_spawn(self, row, column, team):
        self._check_position(row, column)
        position = (row, column)
        positions_spawn = self._get_adjacents_pos(position)
        positions_spawn.append(position)
        if team == Team.IceTeam:
            self.ice_spawn = IceSpawn(positions=positions_spawn, board=self.board)
        else:
            self.fire_spawn = FireSpawn(positions=positions_spawn, board=self.board)
        spawn = self.ice_spawn if team == Team.IceTeam else self.fire_spawn
        self.board.add_spawn(positions=positions_spawn, spawn=spawn)
        self.mode = GameMode.SIMULATION

    def _check_position(self, row, column):
        length = len(self.board)
        if row == 0 or row == length - 1 or column == 0 or column == length - 1:
            raise ValueError("The position is on the edge of the board")
        
    def add_spawn(self, position):
        positions_spawn = self._get_adjacents_pos(position)
        if self.get_team() == Team.IceTeam:
            spawn = IceSpawn(positions=positions_spawn, board=self.board)
        else:
            spawn = FireSpawn(positions=positions_spawn, board=self.board)
        self.board.add_spawn(positions=positions_spawn, spawn=spawn)
        self.mode = GameMode.SIMULATION
        
    def _get_adjacents_pos(self, pos):
        row, col = pos
        length = len(self.board)
        adjacentList = []
        directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < length and 0 <= new_col < length:
                adjacentList.append((new_row, new_col))
        return adjacentList
            
    def create_cell(self, row, column, team, level, life):
        pos = row, column
        if (level == 1):
           level_enum = Level.LEVEL_1
        if (level == 2):
            level_enum = Level.LEVEL_2
        if (level== 3):
            level_enum = Level.LEVEL_3
        
        #cell_id = self.cell_id_counter  
        #self.cell_id_counter += 1

        if (team == Team.IceTeam):
            #self.board.add_cell(row, column, IceCell(cell_id = cell_id, level=level_enum, life = life, position=pos, board=self.board))
            self.board.add_cell(row, column, IceCell(level=level_enum, life = life, position=pos, board=self.board))
        else:
            #self.board.add_cell(row, column, FireCell(cell_id = cell_id, level=level_enum, life=life, position=pos, board=self.board))
            self.board.add_cell(row, column, FireCell(level=level_enum, life=life, position=pos, board=self.board))

    # FIGTHS    
    def execute_fight_in_position(self, row, col):
        cells = self.board.get_cells(row, col)
        ice_cells = [cell for cell in cells if isinstance(cell, IceCell)]
        fire_cells = [cell for cell in cells if isinstance(cell, FireCell)]
        
        # Order by level and life by descendent order
        ice_cells.sort(key=lambda cell: (cell.get_level(), cell.get_life()), reverse=True)
        fire_cells.sort(key=lambda cell: (cell.get_level(), cell.get_life()), reverse=True)

        while ice_cells and fire_cells:
            ice_cells[0].fight(fire_cells[0])
            ice_cells = [cell for cell in cells if isinstance(cell, IceCell) and cell in self.board.get_cells(row, col)]
            fire_cells = [cell for cell in cells if isinstance(cell, FireCell) and cell in self.board.get_cells(row, col)]

    def execute_fights_in_all_positions(self):
        for row in range(self.board.rows):
            for column in range(self.board.columns):
                self.execute_fight_in_position(row, column)
                
    # MOVEMENT
    def move_cells_in_position(self, row, column):
        cells = self.board.get_cells(row, column)
        while len(cells) != 0:
            cell = cells[0]
            self.advance(cell)
            self.board.add_cell_by_tuple(cell.position, cell)
            self.board.remove_cell(row, column, cell)
            
    def execute_movements_in_all_positions(self):
        for row in range(self.board.rows):
            for column in range(self.board.columns):
                self.move_cells_in_position(row, column)
    
    def advance(self, cell):
        if cell.get_position() is not None and self.board is not None:
            tuplePos = cell.get_position()
            positionsList = self._get_adjacents_for_move(tuplePos)
            if positionsList:
                cell.set_position(random.choice(positionsList))
                cell.set_life(cell.get_life() - 1)

    #Get a list of adjacent cells to the cell's current position.
    def _get_adjacents_for_move(self, posXY):
        row, col = posXY
        length = len(self.board)
        adjacentList = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < length and 0 <= new_col < length:
                if (self.no_spawns_in_pos(new_row, new_col)):
                    adjacentList.append((new_row, new_col))
        return adjacentList
    
    def no_spawns_in_pos(self, row, column):
        cells = self.board.get_cells(row, column)
        for cell in cells:
            if (isinstance(cell, Spawn)):
                return False
        return True
    
    # FUSION
    def fusion(self, pos):
        merged = True
        while merged:
            merged = False
            cells_aux = self.board.get_cells(pos[0], pos[1])
            if (len(cells_aux) == 1) : 
                break
            cells_aux = sorted(cells_aux, key=lambda cell: (isinstance(cell, IceCell), isinstance(cell, FireCell), cell.get_level()))
            for i in range(len(cells_aux)-1):
                merged = self.board.fusion(cells_aux[i], cells_aux[i+1])
                if (merged):
                    break

    def execute_fusions_in_all_positions(self):
        for row in range(self.board.rows):
            for column in range(self.board.columns):
                pos = (row, column)
                self.fusion(pos)
        

    def get_mode(self):
        return self.mode
    
    def get_board(self):
        return self.board
    
    def get_team(self):
        return self.team
    
    def get_cells(self, row, column):
        return self.get_board().get_cells(row, column)