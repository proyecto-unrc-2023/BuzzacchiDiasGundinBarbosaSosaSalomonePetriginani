import random
from abc import ABC, abstractmethod
from logic.cell import Cell, Level, FireCell, IceCell

class Spawn:
    
    def __init__(self, life=None, position=None, board=None):
        self.life = life
        self.position = position
        self.board = board
        
    def set_life(self, life):
        self.life = life
        
    def set_board(self, board):
        self.board = board
        
    def decrease_life(self, damage):
        life -= damage
    
    def __str__(self):
        return 'SP' 
    
    def get_adjacents(self, posXY):
        row, col = posXY
        length = len(self.board)
        adjacentList = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < length and 0 <= new_col < length:
                cell = self.board.get_cells(new_row, new_col)
                if (str(cell) == ' '):
                    adjacentList.append(cell)
        return adjacentList
    
    def generate_cells(self):
        if self.position is not None:
            tuplePos = self.position
            positionsList = self.get_adjacents_for_move(tuplePos)
            cantCells = random.randint(0,4)
            for i in range(cantCells):
                position = random.choice(positionsList)
                positionsList.remove(position)
                Cell.__init__(1, 20, position, self.board)
    
    @staticmethod
    def from_string(spawn_str):
        if spawn_str == IceSpawn().__str__():
            return IceSpawn()
        elif spawn_str == FireSpawn().__str__():
            return FireSpawn()
        else:
            raise ValueError(f'Invalid spawn string: {spawn_str}')

class FireSpawn(Spawn):
    def __init__(self, life=None, position=None, board=None):
        self.life = life
        self.position = position
        self.board = board
        
    def set_life(self, life):
        self.life = life
        
    def set_board(self, board):
        self.board = board
        
    def decrease_life(self, damage):
        life -= damage
    
    def __str__(self):
        return 'FS'
    
    def __eq__(self, other):
        return isinstance(other, FireSpawn)    
    
    def generate_cells(self):
        if self.position is not None:
            tuplePos = self.position
            positionsList = self.get_adjacents_for_move(tuplePos)
            cantCells = random.randint(0,4)
            for i in range(cantCells):
                position = random.choice(positionsList)
                positionsList.remove(position)
                FireCell.__init__(1, 20, position, self.board)

class IceSpawn(Spawn):
    def __str__(self):
        return 'IS'
    
    def __eq__(self, other):
        return isinstance(other, IceSpawn)
    
    def __init__(self, life=None, position=None, board=None):
        self.life = life
        self.position = position
        self.board = board
        
    def set_life(self, life):
        self.life = life
        
    def set_board(self, board):
        self.board = board
        
    def decrease_life(self, damage):
        life -= damage
        
    def generate_cells(self):
        if self.position is not None:
            tuplePos = self.position
            positionsList = self.get_adjacents_for_move(tuplePos)
            cantCells = random.randint(0,4)
            for i in range(cantCells):
                position = random.choice(positionsList)
                positionsList.remove(position)
                IceCell.__init__(1, 20, position, self.board)