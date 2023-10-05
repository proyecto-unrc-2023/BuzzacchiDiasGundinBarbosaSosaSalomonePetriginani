#from logic.board import Board
from abc import ABC, abstractmethod
from random import random
from enum import IntEnum

class Level(IntEnum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3

    #Level_1: (0,20] ; Level_2: (20,40] ; Level_3: (40,60]
    @staticmethod
    def life_validation(level, life):
        if level == Level.LEVEL_1 and (life < 0 or life > 20):
            raise ValueError("Life invalid for level 1")
        elif level == Level.LEVEL_2 and (life <= 20 or life > 40):
            raise ValueError("Life invalid for level 2")
        elif level == Level.LEVEL_3 and (life <= 40 or life > 60):
            raise ValueError("Life invalid for level 3")
        return True

class Cell:

    def __init__(self, level=Level.LEVEL_1, life=20, position=None, board=None):
        self.set_level(level)
        self.set_life(life)        
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

    ####  Getters  ####
    def set_position(self, position):
        self.position = position
    
    def set_life(self, life):
        if not Level.life_validation(self.level, life):
            raise ValueError("Invalid life")
        self.life = life

    def set_level(self, level):
        if level is None:
            raise ValueError("Level cant be none")
        if level not in Level:
            raise ValueError("Level must be in [1,2,3]")
        self.level = level
        
    ####  Getters  ####
    def get_level(self):
        return self.level
    
    def get_life(self):
        return self.life
    
    def get_position(self):
        return self.position

    #Move the cell to one of its adjacent positions if possible
    #return adjacent cell selected
    def advance(self):
        if self.position is not None and self.board is not None:
            tuplePos = self.position
            positionsList = self.get_adjacents_for_move(tuplePos)
            if positionsList:
                return random.choice(positionsList)
        return None

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
    
    def level_up(self):
        if self.level == Level.LEVEL_1:
            self.set_level(Level.LEVEL_2)
        elif self.level == Level.LEVEL_2:
            self.set_level(Level.LEVEL_3)
        else:
            raise Exception('Level_3 cannot be level up')

    def fight(self, other_cell):
        if self.position == other_cell.position:
            position = self.position
            if type(self) != type(other_cell):
                # Compare Life Points 
                if(self.get_life() < 4 or other_cell.get_life() < 4):
                    self.board.convert_position_to_dead_cell(position[0],position[1])
                else:
                    # Compare cell levels
                    if self.get_level() > other_cell.get_level():
                        # Remove the other cell from the position
                        self.board.remove_cell(position[0], position[1], other_cell)
                        self.life -= 4
                    elif self.get_level() < other_cell.get_level():
                        # Remove self from the position
                        self.board.remove_cell(position[0], position[1], self)
                        other_cell.life -= 4
                    else:
                        # If levels are equal, compare cell life
                        if self.get_life() > other_cell.get_life():
                            # Remove the other cell from the position
                            self.board.remove_cell(position[0], position[1], other_cell)
                            self.life -= 4
                        elif self.get_life() < other_cell.get_life():
                            # Remove self from the position
                            self.board.remove_cell(position[0], position[1], self)
                            other_cell.life -= 4
                        else:
                            # If both levels and life are equal, convert both cells to dead
                            self.board.convert_position_to_dead_cell(position[0], position[1])
            if self in self.board.get_cells(position[0], position[1]):
                self.modify_cell_after_fight(self)
            else:
                other_cell.modify_cell_after_fight(other_cell)

    #should verify if it is nedeed to modify level of winning cell
    def modify_cell_after_fight(self, cell):
        if (cell.get_level() == Level.LEVEL_3 and cell.get_life() < 40):
            cell.set_level(Level.LEVEL_2)
        if (cell.get_level() == Level.LEVEL_2 and cell.get_life() < 20):
            cell.set_level(Level.LEVEL_1)


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
