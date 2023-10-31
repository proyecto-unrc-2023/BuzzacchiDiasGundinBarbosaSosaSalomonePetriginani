import random 
from abc import ABC, abstractmethod
from logic.cell import Cell, Level, FireCell, IceCell

class Spawn:
    
    def __init__(self, life=300, positions=None):
        self.life = life
        self.positions = positions
        self.type = self.get_type()
        
    def set_life(self, life):
        self.life = life
        
    def set_board(self, board):
        self.board = board
        
    def set_position(self, pos):
        self.positions = pos
    
 #   def set_board(self, board):
 #       self.board = board
 #       
    def get_positions(self):
        return self.positions

    def get_life(self):
        return self.life
        
    def decrease_life(self, damage):
        self.life -= damage
        if(self.life < 0):
            self.life = 0
    
    def __str__(self):
        return 'SP' 
    
    def get_adjacents_spawn(self, length):
        row, col = self.positions[4]
        adjacentList = []
        directions = [(-1, -2), (-2, -2), (-2, -1), (-2, 0), (-2, -1), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (2, -1), (2, -2), (1, -2), (0, -2)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < length and 0 <= new_col < length:
                adjacentList.append((new_row, new_col))
        return adjacentList
        
    def get_adjacents_for_move(self, posXY):
        row, col = posXY
        length = len(self.board)
        adjacentList = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < length and 0 <= new_col < length:
                adjacentList.append((new_row, new_col))
        return adjacentList
    
    def get_type(self):
        return 'Spawn'

    def generate_cells(self):
        if self.positions is None:
            raise ValueError("Posición inválida")
        else:
            positionsList = self.get_adjacents_spawn()
            cantCells = random.randint(1,4)
            retListCells = []
            for i in range(cantCells + 1):
                positions = random.choice(positionsList)
                positionsList.remove(positions)
                retListCells.append(positions)
            return retListCells

    def fight(self, cell):
        new_life = self.get_life() - cell.get_life()
        if new_life > 0:
            self.set_life(new_life)
        else:
            self.set_life(0)
    
    @staticmethod
    def from_string(spawn_str):
        if spawn_str == Spawn().__str__():
            return Spawn()
        elif spawn_str == IceSpawn().__str__():
            return IceSpawn()
        elif spawn_str == FireSpawn().__str__():
            return FireSpawn()
        else:
            raise ValueError(f'Invalid spawn string: {spawn_str}')

class FireSpawn(Spawn):
        
    def set_life(self, life):
        self.life = life
        
    def set_board(self, board):
        self.board = board
        
    def decrease_life(self, damage):
        self.life -= damage
        if(self.life < 0):
            self.life = 0
    
    def __str__(self):
        return 'FS'
    
    def get_type(self):
        return 'FireSpawn'
    
    def __eq__(self, other):
        return isinstance(other, FireSpawn)    
    
    def generate_cell(self):
        if self.positions is not None:
            positionsList = []
            tuplePos = self.positions
            for pos in tuplePos:
                list = self.get_adjacents_spawn()
                if list:
                    positionsList.append(list)
                    pos = random.choice(positionsList)
                cell = (FireCell(positions = pos, board = self.board))
            return cell  

class IceSpawn(Spawn):
    def __str__(self):
        return 'IS'
    
    def __eq__(self, other):
        return isinstance(other, IceSpawn)
        
    def set_life(self, life):
        self.life = life
        
    def set_board(self, board):
        self.board = board
        
    def decrease_life(self, damage):
        self.life -= damage
        if(self.life < 0):
            self.life = 0
    
    def generate_cell(self):
        if self.positions is not None:
            positionsList = []
            tuplePos = self.positions
            for pos in tuplePos:
                list = self.get_adjacents_spawn()
                if list:
                    positionsList.append(list)
                    positions = random.choice(positionsList)
                cell = (IceCell(positions = positions, board = self.board))
            return cell    
    def get_type(self):
        return 'IceSpawn'