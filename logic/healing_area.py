from logic.cell import Cell, Level

class HealingArea:
    
    def __init__(self, positions, affected_cell_type):
        self.positions = positions
        self.duration = 100  
        self.healing_rate = 3  
        self.affected_cell_type = affected_cell_type  
    
    def get_positions(self):
        return self.positions

    def apply_effect(self, cells):
        if self.duration > 0:
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


    def get_type(self):
        if self.affected_cell_type == 'IceCell':
            return 'IceHealingArea'
        else:
            return 'FireHealingArea'
        
    def __str__(self):
        if self.affected_cell_type == 'IceCell':
            return 'IH'
        else:
            return 'FH'
    
    def get_affected_cell_type(self):
        return self.affected_cell_type
'''                            
cell.level_up()
#try:
cell.set_life(cell.get_life() + self.healing_rate)
#except ValueError as e:
#    print(f"Error al establecer la vida de la célula después de aumentar el nivel: {e}")
'''