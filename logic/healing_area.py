from logic.cell import Cell, Level
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
                cells = self.board.get_cells(*position)
                for cell in cells:
                    if isinstance(cell, self.affected_cell_type):
                        try:
                            new_life = cell.get_life() + self.healing_rate
                            if cell.get_level() == Level.LEVEL_3 and new_life > 60:
                                cell.set_life(60)
                                continue
                            cell.set_life(new_life)
                        except ValueError:
                            cell.level_up()
                            cell.set_life(cell.get_life() + self.healing_rate)
            self.duration -= 1

'''                            
cell.level_up()
#try:
cell.set_life(cell.get_life() + self.healing_rate)
#except ValueError as e:
#    print(f"Error al establecer la vida de la célula después de aumentar el nivel: {e}")
'''