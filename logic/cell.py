#from logic.board import Board
from abc import ABC, abstractmethod

from enum import IntEnum
#from api.games.game import CellSchema

LIFE_LOSS_PER_FIGHT = 4
CELL_DEAD = 0

class Level(IntEnum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    
    @staticmethod
    def max_life_level(level):
        if (level == Level.LEVEL_1):
            return 20
        elif (level == Level.LEVEL_2):
            return 40
        elif(level==Level.LEVEL_3):
            return 60
        
    @staticmethod
    def update_level(cell):
        life = cell.get_life()
        if 0 < life <= 20:
            cell.set_level(Level.LEVEL_1)
        elif 20 < life <= 40:
            cell.set_level(Level.LEVEL_2)
        elif 40 < life <= 60:
            cell.set_level(Level.LEVEL_3)

    def __eq__(self, other):
        if isinstance(other, Level):
            return self.value == other.value
        return False
class Cell:

    def __init__(self, level=Level.LEVEL_1, life=20, position=None):
        self.set_level(level)
        self.set_life(life)        
        self.position = position
        self.type = self.get_type()

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

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.level == other.level and self.life == other.life and self.type == other.type #and self.position == other.position
        return False
    
    #<
    def __lt__(self, other_cell):
        if self.level != other_cell.level:
            return self.level > other_cell.level
        else:
            return self.life > other_cell.life

    ####  Getters  ####
    def set_position(self, position):
        self.position = position

    def set_life(self, life):
        self.life = life
        Level.update_level(self)

    def set_level(self, level):
        if Level(level) not in Level:
            raise ValueError(f"Invalid level: {level}")
        self.level = level
        
    ####  Getters  ####
    def get_level(self):
        return self.level
    
    def get_life(self):
        return self.life
    
    def get_position(self):
        return self.position
    
    def get_type(self):
        return 'Cell'
        
    def is_alive(self):
        return self.get_life() > 0
    
    #Comments should be done in another class
    # def level_and_life_up(self):
    #     if (self.level != 3):
    #         self.level_up()
    #         self.life = Level.max_life_level(self.level)
    #         return True
    #     else:
    #         return False

    def fight(self, other_cell):
        if type(self) != type(other_cell):
            if(self.get_life() < LIFE_LOSS_PER_FIGHT or other_cell.get_life() < LIFE_LOSS_PER_FIGHT):
                self.set_life(CELL_DEAD)
                other_cell.set_life(CELL_DEAD)
            else:
                # Compare cell levels
                if self.get_level() > other_cell.get_level():
                    other_cell.set_life(CELL_DEAD)
                    self.set_life(self.get_life() - LIFE_LOSS_PER_FIGHT)
                elif self.get_level() < other_cell.get_level():
                    # Remove self from the position
                    self.set_life(CELL_DEAD)
                    other_cell.set_life(other_cell.get_life() - LIFE_LOSS_PER_FIGHT)
                else:
                    # If levels are equal, compare cell life
                    if self.get_life() > other_cell.get_life():
                        # Remove the other cell from the position
                        other_cell.set_life(CELL_DEAD)
                        self.set_life(self.get_life() - LIFE_LOSS_PER_FIGHT)
                    elif self.get_life() < other_cell.get_life():
                        # Remove self from the position
                        self.set_life(CELL_DEAD)
                        other_cell.set_life(other_cell.get_life() - LIFE_LOSS_PER_FIGHT)
                    else:
                        # If both levels and life are equal, convert both cells to dead
                        self.set_life(CELL_DEAD)
                        other_cell.set_life(CELL_DEAD)

                           
class DeadCell(Cell):

    def __str__(self):
        return ' '

    def get_type(self):
        return 'DeadCell'
    
class IceCell(Cell):

    def __str__(self):
        return 'I'
    
    def get_type(self):
        return 'IceCell'
    
    @classmethod
    def create_from_dict(cls, dict):
        if dict is not None:
            return cls(dict['level'], dict['life'], dict['position'])
        else:
            return None

class FireCell(Cell):

    def __str__(self):
        return 'F'

    def get_type(self):
        return 'FireCell'
    
    @classmethod
    def create_from_dict(cls, dict):
        if dict is not None:
            return cls(dict['level'], dict['life'], dict['position'])
        else:
            return None
