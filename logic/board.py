
from logic.cell import IceCell, FireCell, Cell, DeadCell, Level
from logic.spawn import Spawn, IceSpawn, FireSpawn
from logic.box import Box
from logic.healing_area import HealingArea

class Board:

    def __init__(self, rows, columns, board=None):
        self.rows = rows
        self.columns = columns
        if board is not None:
            self.board = board
        else:
            self.board = [[Box() for _ in range(columns)] for _ in range(rows)]

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

    @staticmethod
    def from_string(board_str):
        board_rows = board_str.split('\n')
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
                    # Add more elif conditions here for other cell types
                    else:
                        raise ValueError("Unknown object type: " + box_str)
                new_board.board[i][j] = new_box
        return new_board
        
    def add_cell(self, row, column, cell):
        cell.set_board(self)
        pos = (row, column)
        cell.set_position(pos)
        box = self.get_box(row, column)
        if isinstance(cell, FireCell):
            box.add_fire_cell(cell)
        elif isinstance(cell, IceCell):
            box.add_ice_cell(cell)

    def get_cells(self, row, column):
        return self.get_box(row,column).get_cells()
    
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

    def convert_two_cells_to_dead_cell(self, row, column, cell, other_cell):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            # Check if the cells exist in the position
            cells_in_position = self.get_cells(row, column)
            if cell not in cells_in_position or other_cell not in cells_in_position:
                raise ValueError("One or both cells not found in the given position")

            # Remove cell and other cell from the position
            self.remove_cell(row, column, cell)
            self.remove_cell(row, column, other_cell)

            # Check if there are any cells left in the position
            if not self.get_cells(row, column):
                # If no cells left, add a dead cell to the position
                dead_cell = DeadCell(position=(row,column), board=self)
                self.add_cell(row, column, dead_cell)
        else:
            raise ValueError("Invalid row or column")

    def add_spawn(self, positions, spawn):
        for pos in positions:
            row, column = pos
            self.board[row][column].append(spawn)
            
    def add_healing_area(self, healing):
        positions = healing.get_positions()
        for pos in positions:
            row, column = pos
            self.board[row][column].append(healing)

