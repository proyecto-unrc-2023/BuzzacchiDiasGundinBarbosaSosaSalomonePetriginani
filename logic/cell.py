
from abc import ABC, abstractmethod


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
