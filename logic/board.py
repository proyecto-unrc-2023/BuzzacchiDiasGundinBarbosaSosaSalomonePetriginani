
from logic.cell import IceCell, FireCell, Cell, DeadCell, Level
from logic.spawn import Spawn, IceSpawn, FireSpawn

class Board:

    def __init__(self, rows, columns, board=None):
        self.rows = rows
        self.columns = columns
        if board is not None:
            self.board = board
        else:
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
    
    def fusion(self, cell1, cell2):
        if(cell1.get_level() != cell2.get_level()):
            return False
        if(cell1.get_level() == Level.LEVEL_1):
            cell1.set_level(Level.LEVEL_2)
            cell1.set_life(40)
            cell1.board.remove_cell(cell1.get_position()[0], cell1.get_position()[1], cell2)
            return True
        elif(cell1.get_level() == Level.LEVEL_2):
            cell1.set_level(Level.LEVEL_3)
            cell1.set_life(60)
            cell1.board.remove_cell(cell1.get_position()[0], cell1.get_position()[1], cell2)
            return True
        return False
                
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
        for position in positions:
            row, column = position
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
            ice_cells = [cell for cell in cells if isinstance(cell, IceCell) and cell in self.get_cells(row, col)]
            fire_cells = [cell for cell in cells if isinstance(cell, FireCell) and cell in self.get_cells(row, col)]

    def execute_fights_in_all_positions(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.execute_fight_in_position(row, column)

    def move_cells_in_position(self, row, column):
        cells = self.get_cells(row, column)
        while len(cells) != 0:
            cell = cells[0]
            cell.advance()
            self.add_cell_by_tuple(cell.position, cell)
            self.remove_cell(row, column, cell)
            
    def execute_movements_in_all_positions(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.move_cells_in_position(row, column)