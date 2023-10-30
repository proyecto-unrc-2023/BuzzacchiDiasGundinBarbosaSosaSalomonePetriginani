from enum import Enum
import random

from logic.cell import IceCell, FireCell, Level
from logic.board import Board
from logic.box import Box
from logic.spawn import Spawn, IceSpawn, FireSpawn
from logic.healing_area import HealingArea

class GameMode(Enum):
    NOT_STARTED = "NOT_STARTED"
    SPAWN_PLACEMENT = "SPAWN_PLACEMENT"
    SIMULATION = "SIMULATION"
    FINISHED = "FINISHED"

    def to_json(self):
        return self.value

class Team(Enum):
    IceTeam = "IceTeam"
    FireTeam = "FireTeam"

    def to_json(self):
        return self.value

class GameState:

    def __init__(self, mode = GameMode.NOT_STARTED, board = None, team = None, username = None, ice_spawn = None, fire_spawn = None, ice_healing_area = None, fire_healing_area = None):
        self.mode = mode
        self.board = board
        self.team = team
        self.username = username
        self.ice_spawn = ice_spawn
        self.fire_spawn = fire_spawn
        self.ice_healing_area = ice_healing_area
        self.fire_healing_area = fire_healing_area
        #self.cell_id_counter = 1

    def new_game(self, rows, columns):
        self.board = Board(rows, columns)
        # self._add_healing_area(Team.IceTeam)
        # self._add_healing_area(Team.FireTeam)
        self.mode = GameMode.SPAWN_PLACEMENT
        
    def set_board(self, board):
        self.board = board

    def set_username(self, username):
        self.username = username

    def set_team(self, team):
        self.team = team
   
    def set_mode(self, mode):
        self.mode = mode

    def get_board(self):
        return self.board
    
    def get_cells(self, row, column):
        return self.get_board().get_box(row,column).get_cells()
    
    def get_ice_cells(self, row, column):
        return self.get_board().get_box(row,column).get_ice_cells()
    
    def get_fire_cells(self, row, column):
        return self.get_board().get_box(row,column).get_fire_cells()
    
    def get_ice_spawn(self):
        return self.ice_spawn
    
    def get_fire_spawn(self):
        return self.fire_spawn
    
    def get_spawn(self, spawn_type):
        return self.get_ice_spawn() if eval(spawn_type) == IceSpawn else self.get_fire_spawn()
    
    def get_mode(self):
        return self.mode
    
    def get_team(self):
        return self.team
    
    def add_cell(self, row, column, cell):
        self.board.add_cell(row, column, cell)

    def remove_cell(self, row, column, cell):
        self.board.remove_cell(row, column, cell)

    def get_cells_in_spawn(self, spawn):
        spawn = self.ice_spawn if spawn.get_type() == 'IceSpawn' else self.fire_spawn
        positions = spawn.get_positions()
        cells_in_spawn = []
        for position in positions:
            cells_in_position = self.get_cells(*position)
            for cell in cells_in_position:
                if isinstance(cell, FireCell) or isinstance(cell,IceCell):
                    cells_in_spawn.append(cell)
        return cells_in_spawn
            
    def create_healing_area(self, row, column, affected_cell_type):
        if affected_cell_type == IceCell:
            self.ice_healing = self.board.create_healing_area(row, column, affected_cell_type)
        else:
            self.fire_healing = self.board.create_healing_area(row, column, affected_cell_type)

    def create_cell(self, row, column, cell_type, level=Level.LEVEL_1, life=20):
        pos = row, column
        if (level == 1):
           level_enum = Level.LEVEL_1
        if (level == 2):
            level_enum = Level.LEVEL_2
        if (level== 3):
            level_enum = Level.LEVEL_3

        if (cell_type == IceCell):
            self.add_cell(row, column, (IceCell(level=level_enum, life = life, position=pos)))
        else:
            self.add_cell(row, column, (FireCell(level=level_enum, life=life, position=pos)))

    def create_spawn(self, row, column, spawn_team):
        if spawn_team == IceSpawn:
            self.ice_spawn = self.board.create_spawn(row, column, spawn_team)
        else:
            self.fire_spawn = self.board.create_spawn(row, column, spawn_team)
        self.create_inverse_spawn(row, column, spawn_team)
        self.check_simulation()
    
    def execute_fight_in_position(self, row, col):
        ice_cells = self.board.get_ice_cells(row, col)
        fire_cells = self.board.get_fire_cells(row, col)
        spawn = self.board.get_spawn(row, col)

        if not spawn:
            while ice_cells and fire_cells:
                index = 0
                ice_cells[index].fight(fire_cells[index])
                if ice_cells[index].is_alive():
                    self.remove_cell(row, col, fire_cells[index])
                else:
                    self.remove_cell(row, col, ice_cells[index])
                index += 1
        else:
            #Fight spawns
            if spawn.get_type() == 'IceSpawn':
                for fire_cell in fire_cells.copy():
                    spawn.fight(fire_cell)
                    self.remove_cell(row, col, fire_cell)
            else:
                for ice_cell in ice_cells.copy():
                    spawn.fight(ice_cell)
                    self.remove_cell(row, col, ice_cell)
            if spawn.get_life() == 0:
                self.set_mode(GameMode.FINISHED)

    def execute_fights_in_all_positions(self):
        for row in range(self.board.rows):
            for column in range(self.board.columns):
                self.execute_fight_in_position(row, column)
                
    # MOVEMENT
    # Copy of list created because of an infinite loop
    def move_cells_in_position(self, row, column):
        cells = list(self.board.get_cells(row, column))  
        while len(cells) != 0:
            cell = cells[0]
            self.advance(cell)
            self.board.add_cell(*cell.get_position(), cell)
            self.board.remove_cell(row, column, cell)
            cells.remove(cell)  
            
    def execute_movements_in_all_positions(self):
        for row in range(self.board.rows):
            for column in range(self.board.columns):
                self.move_cells_in_position(row, column)
    
    def advance(self, cell):
        if cell.get_position() is not None and self.board is not None:
            if isinstance(cell, IceCell):    
                cell_team = Team.IceTeam
            else:
                cell_team = Team.FireTeam    
            tuplePos = cell.get_position()
            positionsList = self.get_adjacents_for_move(tuplePos, cell_team)
            if positionsList:
                cell.set_position(random.choice(positionsList))
                if cell.get_life() > 0:
                    cell.set_life(cell.get_life() - 1)

    #Get a list of adjacent cells to the cell's current position.
    def get_adjacents_for_move(self, posXY, cell_team):
        row, col = posXY
        length = len(self.board)
        adjacentList = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < length and 0 <= new_col < length:
                if (self.no_spawns_in_pos(new_row, new_col, cell_team)):
                    adjacentList.append((new_row, new_col))
        return adjacentList
    
    def no_spawns_in_pos(self, row, column, cell_team):
        cells = self.board.get_cells(row, column)
        for cell in cells:
            if cell_team == Team.IceTeam:   
                if (isinstance(cell, IceSpawn)):
                    return False
            else:
                if (isinstance(cell, FireSpawn)):
                    return False   
        return True
    
    # FUSION
    def fusion(self, pos):
        box = self.board.get_box(pos[0], pos[1])
        cells_ice_aux =  box.get_ice_cells()
        cells_fire_aux = box.get_fire_cells()
        remove_this_cells = []
        # print("Comienzo de Fusion")
        #For Ice Cells
        count_fusion = 1
        # if(cells_ice_aux):
        #     print("entre al if de ice")
        while(count_fusion > 0):
        # print("entre al while de ice")
            count_fusion = 0
            remove_this_cells.clear()
            for i in range(len(cells_ice_aux)-1):
                print("entre al for de ice")
                if (cells_ice_aux[i].get_level() == cells_ice_aux[i+1].get_level()):
                    print("Entre al if level del ice")
                    merged = cells_ice_aux[i+1].level_and_life_up()
                    if(merged):
                        remove_this_cells.append(cells_ice_aux[i])
                        count_fusion += 1
                    print("merge un Ice")
            for cell in remove_this_cells:
                print("se elimino .Ice")
                print(cell)
                self.board.remove_cell(pos[0], pos[1], cell)
        # For Fire Cells
        count_fusion = 1
        # if(cells_fire_aux):
        #     print("entre al if de fire")
        while(count_fusion > 0):
            count_fusion = 0
            remove_this_cells.clear()
            for i in range(len(cells_fire_aux)-1):
                if (cells_fire_aux[i].get_level() == cells_fire_aux[i+1].get_level( )):
                    merged = cells_fire_aux[i+1].level_and_life_up()
                    if(merged):
                        remove_this_cells.append(cells_fire_aux[i])
                        count_fusion += 1
                    print("merge un Fire")
            for cell in remove_this_cells:
                print("se elimino .Fire")
                print(cell)
                self.board.remove_cell(pos[0], pos[1], cell)
    
        
        # merged = True
        # while merged:
        #     merged = False
        #     cells_aux = self.board.get_cells(pos[0], pos[1])
        #     if (len(cells_aux) == 1) : 
        #         break
        #     cells_aux = sorted(cells_aux, key=lambda cell: (isinstance(cell, IceCell), isinstance(cell, FireCell), cell.get_level()))
        #     for i in range(len(cells_aux)-1):
        #         if (cells_aux[i].get_level() == cells_aux[i+1])
        #         merged = cells_aux[i].fusion(cells_aux[i+1])
        #         if (merged):
        #             break

    def execute_fusions_in_all_positions(self):
        for row in range(self.board.rows):
            for column in range(self.board.columns):
                pos = (row, column)
                self.fusion(pos)
    
    def generate_cell(self):
        for row in range(self.board.rows):
            for column in range(self.board.columns):
                list = self.get_cells(row, column)
                if list is not None:
                    for cell in list:
                        if isinstance(cell, Spawn):
                            spawn = cell
        num = random.randint(1,4)
        for j in range(num):
            cell = spawn.generate_cell()
            r, c = cell.get_position()
            self.get_board().add_cell(r, c, cell)

    def check_simulation(self):
        if self.ice_spawn is not None and self.fire_spawn is not None: 
            self.set_mode(GameMode.SIMULATION)

    def create_inverse_spawn(self, row, column, spawn_team):
        board_rows = self.board.__len__()
        board_columns = self.board.get_columns()
        
        inverse_row = board_rows - row - 1 
        inverse_column = board_columns - column -1

        if spawn_team == IceSpawn:
            self.fire_spawn = self.board.create_spawn(inverse_row, inverse_column, FireSpawn)
        else:
            self.ice_spawn = self.board.create_spawn(inverse_row, inverse_column, IceSpawn)