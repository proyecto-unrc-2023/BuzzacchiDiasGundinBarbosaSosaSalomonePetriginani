
from abc import ABC, abstractmethod

class Spawn:
    
    def __init__(self, life=None, position=None):
        self.life = life
        self.position = position
    
    def __str__(self):
        raise NotImplementedError      
    
    @staticmethod
    def from_string(spawn_str):
        if spawn_str == IceSpawn().__str__():
            return IceSpawn()
        elif spawn_str == FireSpawn().__str__():
            return FireSpawn()
        else:
            raise ValueError(f'Invalid spawn string: {spawn_str}')

class FireSpawn(Spawn):
    
    def __str__(self):
        return 'FS'
    
    def __eq__(self, other):
        return isinstance(other, FireSpawn)    

class IceSpawn(Spawn):
    def __str__(self):
        return 'IS'
    
    def __eq__(self, other):
        return isinstance(other, IceSpawn)