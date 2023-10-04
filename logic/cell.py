#from logic.board import Board
from abc import ABC, abstractmethod
from random import random

class Cell:

    def __init__(self, level=None, life=None, position=None, board=None):
        self.level = level
        self.life = life
        self.position = position
        self.board = board

    @staticmethod
    def from_string(cell_str):
        if cell_str == IceCell().__str__():
            return IceCell()
        elif cell_str == FireCell().__str__():
            return FireCell()
        elif cell_str == DeadCell().__str__():
            return DeadCell()
        else:
            raise ValueError(f'Invalid cell string: {cell_str}')

    def __str__(self):
        raise NotImplementedError

    def set_position(self, position):
        self.position = position

    #Move the cell to one of its adjacent positions if possible
    #return adjacent cell selected
    def advance(self):
        if self.position is not None and self.board is not None:
            tuplePos = self.position
            positionsList = self.get_adjacents_for_move(tuplePos)
            if positionsList:
                self.position = random.choice(positionsList)


    #Get a list of adjacent cells to the cell's current position.
    def get_adjacents_for_move(self, posXY):
        row, col = posXY
        length = len(self.board)
        adjacentList = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < length and 0 <= new_col < length:
                cell = self.board.get_cells(new_row, new_col)
                if (
                    (str(self) == 'F' and str(cell) != 'FS') or
                    (str(self) == 'I' and str(cell) != 'IS') or
                    str(cell) == ' '
                ):
                    adjacentList.append(cell)
        return adjacentList

class DeadCell(Cell):

    def __str__(self):
        return ' '

    def __eq__(self, other):
        return self is other


class IceCell(Cell):

    def __str__(self):
        return 'I'

    def __eq__(self, other):
        return self is other

class FireCell(Cell):

    def __str__(self):
        return 'F'

    def __eq__(self, other):
        return self is other
