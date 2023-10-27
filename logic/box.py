from logic.cell import IceCell, FireCell
import bisect

class Box:

    def __init__(self):
        self.spawn = None
        self.fire_cells = []
        self.ice_cells = []
        self.fire_healing_area = None
        self.ice_healing_area = None
        self.pos = None

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
            elements.append(", ".join(str(cell) for cell in self.ice_cells))
        return ",".join(elements)

    def isEmpty(self):
        return not self.spawn and not self.fire_cells and not self.ice_cells and not self.fire_healing_area and not self.ice_healing_area
