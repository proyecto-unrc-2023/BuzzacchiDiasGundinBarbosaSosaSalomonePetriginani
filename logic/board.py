
from logic.cell import IceCell, FireCell, Cell, DeadCell
from logic.spawn import Spawn, IceSpawn, FireSpawn

class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = []
        self.board = [[[] for _ in range(columns)] for _ in range(rows)]

    def __str__(self):
        rows_str = []
        for row in self.board:
            cell_strs = []
            for cell_list in row:
                if not cell_list:
                    cell_strs.append(' ')
                else:
                    cell_strs.append(','.join(str(cell) for cell in cell_list))
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
            row_cells = board_rows[i].split('|')
            for j in range(columns):
                cell_strs = row_cells[j].split(',')
                for cell_str in cell_strs:
                    cell_str = cell_str.strip()
                    if cell_str == '':
                        new_board.add_cell(i, j, DeadCell())
                    elif cell_str == 'F':
                        new_board.add_cell(i, j, FireCell())
                    elif cell_str == 'I':
                        new_board.add_cell(i, j, IceCell())
                    else:
                        raise ValueError("Unknown cell type: " + cell_str)
        return new_board

    def add_cell(self, row, column, cell):
        self.board[row][column].append(cell)

    def add_cell_by_tuple(self, position, cell):
        row, column = position
        self.add_cell(row, column, cell)

    def remove_cell(self, row, column, cell):
        self.board[row][column].remove(cell)

    def get_cells(self, row, column):
        return self.board[row][column]

    def get_pos(self, cell):
        for i, row in enumerate(self.board):
            for j, cell_list in enumerate(row):
                if cell in cell_list:
                    return (i, j)
        return None

    def convert_position_to_dead_cell(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            # Get a copy of cells in given position
            cells_in_position = list(self.get_cells(row, column))

            for cell in cells_in_position:
                self.remove_cell(row, column, cell)

            dead_cell = DeadCell(position=(row,column), board=self)
            self.add_cell(row, column, dead_cell)
        else:
            raise ValueError("Invalid row or column")
    
    def add_spawn(self, row, column, spawn):
        position = (row, column)
        spawn.position = position
        self.board[row][column].append(spawn)

    def execute_fight_in_position(self, row, col):
        cells = self.get_cells(row, col)
        ice_cells = [cell for cell in cells if isinstance(cell, IceCell)]
        fire_cells = [cell for cell in cells if isinstance(cell, FireCell)]
        
        # Order by level and life by descendent order
        ice_cells.sort(key=lambda cell: (cell.get_level(), cell.get_life()), reverse=True)
        fire_cells.sort(key=lambda cell: (cell.get_level(), cell.get_life()), reverse=True)

        while ice_cells and fire_cells:
            ice_cells[0].fight(fire_cells[0])
            ice_cells = [cell for cell in ice_cells if cell in self.get_cells(row, col)]
            fire_cells = [cell for cell in fire_cells if cell in self.get_cells(row, col)]
    def advance(self, cell):
        row = cell.position[0]
        column = cell.position[1]
        self.remove_cell(row, column, cell)
        cell.advance()
        self.add_cell(cell.position[0], cell.position[1], cell)
