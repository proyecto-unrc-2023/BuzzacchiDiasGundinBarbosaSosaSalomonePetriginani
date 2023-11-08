
from logic.cell import IceCell, FireCell
from logic.spawn import IceSpawn, FireSpawn
from logic.box import Box
from logic.healing_area import HealingArea
import json
import random

class Board:

    def __init__(self, rows, columns, board=None):
        self.rows = rows
        self.columns = columns
        if board is not None:
            self.board = board
        else:
            self.board = [[Box() for _ in range(columns)] for _ in range(rows)]
            for i in range(rows):
                for j in range(columns):
                    self.board[i][j].set_pos((i, j))

    def __str__(self):
        rows_str = []
        for row in self.board:
            cell_strs = []
            for box in row:
                if box.isEmpty():
                    cell_strs.append(' ')
                else:
                    cell_strs.append(str(box))
            rows_str.append('|'.join(cell_strs))
        return '\n'.join(rows_str)

    def __len__(self):
        return self.rows

    def get_columns(self):
        return self.columns
    
    @staticmethod
    def from_string(board_str):
        board_rows = [row.rstrip() for row in board_str.split('\n')]  # strip trailing spaces
        rows = len(board_rows)
        columns = len(board_rows[0].split('|'))
        new_board = Board(rows, columns)
        for i in range(rows):
            row_boxes = board_rows[i].split('|')
            for j in range(columns):
                box_strs = row_boxes[j].split(',')
                new_box = Box()
                for box_str in box_strs:
                    box_str = box_str.strip()
                    if box_str == '':
                        continue  
                    elif box_str == 'F':
                        new_box.add_fire_cell(FireCell())
                    elif box_str == 'I':
                        new_box.add_ice_cell(IceCell())
                    elif box_str == 'IS':
                        new_box.set_spawn(IceSpawn())
                    elif box_str == 'FS':
                        new_box.set_spawn(FireSpawn())
                    elif box_str == 'IH':
                        new_box.set_ice_healing_area(HealingArea(affected_cell_type=IceCell))
                    elif box_str == 'FH':
                        new_box.set_fire_healing_area(HealingArea(affected_cell_type=FireCell))
                    else:
                        raise ValueError("Unknown object type: " + box_str)
                new_board.board[i][j] = new_box
        return new_board
        
    def add_cell(self, row, column, cell):
        pos = (row, column)
        cell.set_position(pos)
        box = self.get_box(row, column)
        if isinstance(cell, FireCell):
            box.add_fire_cell(cell)
        elif isinstance(cell, IceCell):
            box.add_ice_cell(cell)

    def get_cells(self, row, column):
        return self.get_box(row,column).get_cells()
    
    def get_ice_cells(self, row, column):
        return self.get_box(row, column).get_ice_cells()
    
    def get_fire_cells(self, row, column):
        return self.get_box(row, column).get_fire_cells()
    
    def get_spawn(self, row, column):
        return self.get_box(row,column).get_spawn()
    
    def remove_cell(self, row, column, cell):
        self.get_box(row, column).remove_cell(cell)

    def get_box(self, row, column):
        return self.board[row][column]

    #Innecesario?
    # def get_pos(self, cell):
    #     for i, row in enumerate(self.board):
    #         for j, cell_list in enumerate(row):
    #             if cell in cell_list:
    #                 return (i, j)
    #     return None

    def _check_position(self, row, column):
        length = len(self.board)
        if row == 0 or row == length - 1 or column == 0 or column == length - 1:
            raise ValueError("The position is on the edge of the board")
        
    def create_spawn(self, row, column, spawn_team):
        self._check_position(row, column)
        position = (row, column)
        positions_spawn = self._get_adjacents_pos(position)
        ice_spawn = None
        fire_spawn = None
        if spawn_team == IceSpawn:
            ice_spawn = IceSpawn(positions=positions_spawn)
        else:
            fire_spawn = FireSpawn(positions=positions_spawn)
        spawn = ice_spawn if ice_spawn else fire_spawn
        self.add_spawn(spawn=spawn)
        return spawn

    def create_healing_area_with_random_position(self, affected_cell_type, ice_spawn_positions, fire_spawn_positions):
        length = len(self.board)-1
        spawn_positions = ice_spawn_positions + fire_spawn_positions

        while True:
            row = random.randrange(1, length)
            column = random.randrange(1, length)
            # Obtener todas las posiciones en el cuadrado de 3x3
            positions_in_square = self._get_adjacents_pos((row, column))
            # Verificar si alguna de las posiciones en el cuadrado es una posición de generación
            if not any(pos in spawn_positions for pos in positions_in_square):
                break

        self._check_position(row, column)
        return self.create_healing_area(row, column, affected_cell_type)
    
    def create_healing_area(self, row, column, affected_cell_type):
        self._check_position(row, column)
        position = (row, column)
        positions_healing = self._get_adjacents_pos(position)
        healing_area = HealingArea(positions=positions_healing, affected_cell_type=affected_cell_type)
        self.add_healing_area(self, healing_area)
        return healing_area
    
    def delete_healings_area(self, row, column):
        self.get_box(row, column).remove_healings_area(row, column)

    def add_spawn(self, spawn):
        positions_spawn = spawn.get_positions()
        for position in positions_spawn:
            self.get_box(*position).set_spawn(spawn)
        
    def add_healing_area(self, position, healing_area):
        positions_healing = healing_area.get_positions()
        for position in positions_healing:
            self.get_box(*position).set_healing_area(healing_area)
    
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

    @classmethod
    def create_from_dict(cls, dict):
        rows = dict['rows']
        columns = dict['columns']
        board = [[Box.create_from_dict(box_dict) for box_dict in row] for row in dict['board']]
        return cls(rows, columns, board)

    def __eq__(self, other):
        if not isinstance(other, Board):
            return NotImplemented
        if self.rows != other.rows or self.columns != other.columns:
            return False
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != other.board[i][j]:
                    return False
        return True