from logic.cell import Cell, Level, IceCell, FireCell

class HealingArea:
    
    def __init__(self, positions, affected_cell_type, duration=100, healing_rate=3):
        if positions is not None:
            # Convert JSON list representations to tuples for immutable coordinates.
            self.positions = [tuple(position) for position in positions]
        else:
            self.positions = []
        self.duration = duration
        self.healing_rate = healing_rate 
        self.affected_cell_type = affected_cell_type
        self.type = self.get_type()

    def get_positions(self):
        return self.positions
    
    def get_healing_rate(self):
        return self.healing_rate
    
    def get_duration(self):
        return self.duration
    
    def set_healing_rate(self, healing_rate):
        self.healing_rate = healing_rate

    def decrease_duration(self):
        self.duration -= 1
        
    def apply_effect(self, cells):
        if self.duration > 0:
            for cell in cells:
                if isinstance(cell, self.affected_cell_type):
                    new_life = cell.get_life() + self.healing_rate
                    #level = cell.get_level()
                    if new_life > 60:
                        new_life = 60
                    cell.set_life(new_life)
                    (cell.get_level()).update_level(cell)

                    #if new_life > (cell.get_level).max_life_level(cell.get_level):
                    #    if cell.get_level() == Level.LEVEL_1:
                    #        cell.set_level(Level.LEVEL_2)
                    #    elif cell.get_level() == Level.LEVEL_2:
                    #        cell.set_level(Level.LEVEL_3)
                    #    elif cell.get_level() == Level.LEVEL_3:# and new_life > 60:
                    #        new_life = 60
                            #cell.set_life(60)
                            #continue
                    #cell.set_life(new_life)
            #self.duration = self.duration - 1

    def get_type(self):
        if self.affected_cell_type == 'IceCell' or self.affected_cell_type == IceCell:
            return 'IceHealingArea'
        else:
            return 'FireHealingArea'
        
    def __str__(self):
        if self.get_type() == 'IceHealingArea':
            return 'IH'
        else:
            return 'FH'
    
    def get_affected_cell_type(self):
        return self.affected_cell_type
    
    @classmethod
    def create_from_dict(cls, dict):
        if dict is not None:
            return cls(dict['positions'], eval(dict['affected_cell_type']), dict['duration'], dict['healing_rate'])
        else:
            return None
        
    def __eq__(self, other):
        if isinstance(other, HealingArea):
            return (self.positions == other.positions and
                    self.duration == other.duration and
                    self.healing_rate == other.healing_rate and 
                    (self.affected_cell_type == other.affected_cell_type or eval(self.affected_cell_type) == other.affected_cell_type))
        return False
