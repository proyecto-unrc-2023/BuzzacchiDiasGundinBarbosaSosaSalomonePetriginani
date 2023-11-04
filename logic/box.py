from logic.cell import IceCell, FireCell, Cell
from logic.spawn import Spawn, IceSpawn, FireSpawn
from logic.healing_area import HealingArea
import bisect

class Box:

    def __init__(self, spawn=None, fire_cells=None, ice_cells=None, fire_healing_area=None, ice_healing_area=None, pos=None):
        self.spawn = spawn
        self.fire_cells = fire_cells if fire_cells is not None else []
        self.ice_cells = ice_cells if ice_cells is not None else []
        self.fire_healing_area = fire_healing_area
        self.ice_healing_area = ice_healing_area
        self.pos = pos

    # Getter para 'spawn'
    def get_spawn(self):
        return self.spawn

    # Setter para 'spawn'
    def set_spawn(self, value):
        self.spawn = value

    # Getter para 'fire_cells'
    def get_fire_cells(self):
        return self.fire_cells

    # Getter para 'ice_cells'
    def get_ice_cells(self):
        return self.ice_cells

    def get_cells(self):
        return self.ice_cells + self.fire_cells
    
    # Getter para 'fire_healing_area'
    def get_fire_healing_area(self):
        return self.fire_healing_area

    # Setter para 'fire_healing_area'
    def set_fire_healing_area(self, value):
        self.fire_healing_area = value

    # Getter para 'ice_healing_area'
    def get_ice_healing_area(self):
        return self.ice_healing_area

    # Setter para 'ice_healing_area'
    def set_ice_healing_area(self, value):
        self.ice_healing_area = value

    def set_healing_area(self, healing_area):
        if healing_area.get_affected_cell_type() == IceCell:
            self.set_ice_healing_area(healing_area)
        else:
            self.set_fire_healing_area(healing_area)

    # Getter para 'pos'
    def get_pos(self):
        return self.pos

    # Setter para 'pos'
    def set_pos(self, value):
        self.pos = value
    
    def add_cell(self, cell):
        if isinstance(cell, IceCell):
            self.add_ice_cell(cell)
        elif isinstance(cell, FireCell):
            self.add_fire_cell(cell)
        else:
            raise ValueError("Invalid cell type")
    
    def add_ice_cell(self, cell):
        bisect.insort(self.ice_cells, cell)

    def add_fire_cell(self, cell):
        bisect.insort(self.fire_cells, cell)

    def remove_cell(self, cell):
        if isinstance(cell, IceCell):
            self.remove_ice_cell(cell)
        elif isinstance(cell, FireCell):
            self.remove_fire_cell(cell)
        else:
            raise ValueError("Invalid cell type")
        
    def remove_ice_cell(self, cell):
        if cell in self.ice_cells:
            self.ice_cells.remove(cell)

    def remove_fire_cell(self, cell):
        if cell in self.fire_cells:
            self.fire_cells.remove(cell)

    def __str__(self):
        elements = []
        if self.spawn:
            elements.append(str(self.spawn))
        if self.fire_healing_area is not None and self.fire_healing_area.get_type() == 'FireHealingArea':
            elements.append(str(self.fire_healing_area))
        if self.ice_healing_area is not None and self.ice_healing_area.get_type() == 'IceHealingArea':
            elements.append(str(self.ice_healing_area))
        if self.fire_cells:
            elements.append(",".join(str(cell) for cell in self.fire_cells))
        if self.ice_cells:
            elements.append(",".join(str(cell) for cell in self.ice_cells))
        return ",".join(elements)

    def isEmpty(self):
        return not self.spawn and not self.fire_cells and not self.ice_cells and not self.fire_healing_area and not self.ice_healing_area
    
    @classmethod
    def create_from_dict(cls, dict):
        spawn = None
        if dict.get('spawn') is not None:
            if dict['spawn']['type'] == 'IceSpawn':
                spawn = IceSpawn.create_from_dict(dict['spawn'])
            elif dict['spawn']['type'] == 'FireSpawn':
                spawn = FireSpawn.create_from_dict(dict['spawn']) 
        fire_cells = [FireCell.create_from_dict(cell_dict) for cell_dict in dict['fire_cells']]
        ice_cells = [IceCell.create_from_dict(cell_dict) for cell_dict in dict['ice_cells']]
        fire_healing_area = HealingArea.create_from_dict(dict['fire_healing_area'])
        ice_healing_area = HealingArea.create_from_dict(dict['ice_healing_area'])
        pos = tuple(dict['pos'])
        #pos = dict['pos']
        return cls(spawn, fire_cells, ice_cells, fire_healing_area, ice_healing_area, pos)
    
    # def __eq__(self, other):
    #     if isinstance(other, Box):
    #         return (self.spawn == other.spawn and
    #                 self.fire_cells == other.fire_cells and
    #                 self.ice_cells == other.ice_cells and
    #                 self.fire_healing_area == other.fire_healing_area and
    #                 self.ice_healing_area == other.ice_healing_area and
    #                 self.pos == other.pos)
    #     return False

    def __eq__(self, other):
        if not isinstance(other, Box):
            print("Comparison object is not of type Box")
            return False

        if self.spawn != other.spawn:
            print(f"Spawn mismatch: {self.spawn} != {other.spawn}")
            return False
        
        if self.fire_cells != other.fire_cells:
            print(f"Fire cells mismatch: {self.fire_cells} != {other.fire_cells}")
            return False

        if self.ice_cells != other.ice_cells:
            print(f"Ice cells mismatch: {self.ice_cells} != {other.ice_cells} in position {self.pos}")
            return False

        if self.fire_healing_area != other.fire_healing_area:
            print(f"Fire healing area mismatch: {self.fire_healing_area} != {other.fire_healing_area}")
            return False

        if self.ice_healing_area != other.ice_healing_area:
            print(f"Ice healing area mismatch: {self.ice_healing_area} != {other.ice_healing_area}")
            return False

        if self.pos != other.pos:
            print(f"Position mismatch: {self.pos} != {other.pos}")
            return False

        # If all checks pass, then the objects are considered equal.
        return True


