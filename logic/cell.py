#import board
from abc import ABC, abstractmethod
from random import random

class Cell:

    def __init__(self, level=None, life=None, position=None):
        self.level = level
        self.life = life
        self.position = position

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

    def avanzar(self):
        tuplePos = board.get_pos(self)
        positionsList = self.get_adjacents(self, tuplePos)
        posRandom = random.random(positionsList)
        return positionsList[random]

    def get_adjacents(self, posXY):
        row, col = posXY
        length = len(board)
        adjacentList = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < length and 0 <= new_col < length:
                if((self.__str__() == 'F' and board.get_cell(new_row, new_col).__str__() != 'FS') or (self.__str__() == 'I' and board.get_cell(new_row, new_col).__str__() != 'IS') ):
                    adjacentList.append(board[new_row][new_col])
        return adjacentList
class DeadCell(Cell):

    def __str__(self):
        return ' '

    def __eq__(self, other):
        return isinstance(other, DeadCell)


class IceCell(Cell):

    def __str__(self):
        return 'I'

    def __eq__(self, other):
        return isinstance(other, IceCell)

class FireCell(Cell):

    def __str__(self):
        return 'F'

    def __eq__(self, other):
        return isinstance(other, FireCell)
