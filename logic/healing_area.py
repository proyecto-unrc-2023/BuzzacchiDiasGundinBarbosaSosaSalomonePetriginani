from logic.cell import Cell
from logic.board import  Board

class HealingArea:
    
    def __init__(self, board, positions, duration, affected_cell_type):
        self.board = board
        self.positions = positions
        self.duration = duration  
        self.healing_rate = 3  
        self.affected_cell_type = affected_cell_type  

    def apply_effect(self):
        if self.duration > 0:
            for position in self.positions:
                cell = self.board.get_cells(position)
                if isinstance(cell, self.affected_cell_type):
                    cell_life = cell.get_life()
                    cell.set_life(cell_life + self.healing_rate)
            self.duration -= 1
