#Board:
#  - rows
#  - columns
#  - to string
#  - create from string
#  - put live cell

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