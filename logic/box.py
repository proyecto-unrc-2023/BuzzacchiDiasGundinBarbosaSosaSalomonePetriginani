import heapq

class Box:

    def __init__(self):
        spawn = None
        fire_cells = None
        ice_cells = None
        fire_healing_area = None
        ice_healing_area = None
        pos = None

    # Getter para 'spawn'
    def get_spawn(self):
        return self.spawn

    # Setter para 'spawn'
    def set_spawn(self, value):
        self.spawn = value

    # Getter para 'fire_cells'
    def get_fire_cells(self):
        return self.fire_cells

    # Setter para 'fire_cells'
    def set_fire_cells(self, value):
        self.fire_cells = value

    # Getter para 'ice_cells'
    def get_ice_cells(self):
        return self.ice_cells

    # Setter para 'ice_cells'
    def set_ice_cells(self, value):
        self.ice_cells = value

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

    # Getter para 'pos'
    def get_pos(self):
        return self.pos

    # Setter para 'pos'
    def set_pos(self, value):
        self.pos = value

    #add a new cell in ice_cells
    def add_ice_cell(self, cell):
        heapq.heappush(self.ice_cells, cell)

    #add a new cell in fire_cells
    def add_fire_cell(self, cell):
        heapq.heappush(self.fire_cells, cell)

    def __str__(self):
        box_trl = []
        ice_list = []
        fire_list = []
        ice_list.append('')
        for ice_cell in self.ice_cells:
            ice_list.append(heapq.heappop(self.ice_cells + ','))
        ice_list.append('')

        fire_list.append('')
        for fire_cell in self.fire_cells:
            fire_list.append(heapq.heappop(self.fire_cells + ','))
        fire_list.append('')

        box_trl.append(ice_list.append(fire_list))
