
from logic.cell import DeadCell, IceCell, FireCell, Cell

class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = []
        for row in range(self.rows):
            curr_row = []
            for col in range(self.columns):
                curr_row.append(DeadCell())
            self.board.append(curr_row)

    def __str__(self):
        rows_str = ['|'.join(map (str, row)) for row in self.board]
        return '\n'.join(rows_str)

    @staticmethod
    def from_string(board_str):
        board_rows = board_str.split('\n')
        rows = len(board_rows)
        columns = len(board_rows[0].split('|'))
        new_board = Board(rows, columns)
        for i in range(rows):
            row_cells = board_rows[i].split('|')
            for j in range(columns):
                cell_str = row_cells[j]
                if cell_str == str(DeadCell()):
                    new_board.put_cell(i, j, DeadCell())
                elif cell_str == str(FireCell()):
                    new_board.put_cell(i, j, FireCell())
                elif cell_str == str(IceCell()):
                    new_board.put_cell(i, j, IceCell())
                else:
                    raise ValueError("Unknown cell type: " + cell_str)
        return new_board


    def get_cell(self, row, column):
        return self.board[row][column]

    def put_cell(self, row, column, cell):
        self.board[row][column] = cell

    def put_fire_cell(self, row, column):
        if self.get_cell(row, column).__eq__(DeadCell()):
            self.board[row][column] = FireCell()
        else:
            raise ValueError

    def put_ice_cell(self, row, column):
        if self.get_cell(row, column).__eq__(DeadCell()):
            self.board[row][column] = IceCell()
        else:
            raise ValueError
