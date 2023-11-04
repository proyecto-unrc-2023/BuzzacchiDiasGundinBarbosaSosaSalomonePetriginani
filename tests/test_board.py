import pytest

from logic.board import Board
from logic.cell import IceCell, FireCell, Cell
from logic.spawn import IceSpawn, FireSpawn, Spawn
from logic.healing_area import HealingArea
from logic.box import Box

@pytest.fixture
def board():
    return Board(10, 10)

@pytest.fixture
def board_dict():
    return {
        "rows": 2,
        "columns": 2,
        "board": [
            [
                {
                    "spawn": {
                        "life": 300,
                        "positions": [[0, 0],[0, 1],[0, 2],[1, 0],[1, 1],[1, 2],[2, 0],[2, 1],[2, 2]],
                        "type": "IceSpawn"
                    },
                    "fire_cells": [
                        {
                            "level": 1,
                            "life": 18,
                            "position": [0, 0]
                        }
                    ],
                    "ice_cells": [],
                    "fire_healing_area": None,
                    "ice_healing_area": None,
                    "pos": [0, 0]
                },
                {
                    "spawn": None,
                    "fire_cells": [],
                    "ice_cells": [],
                    "fire_healing_area": None,
                    "ice_healing_area": None,
                    "pos": [0, 1]
                }
            ],
            [
                {
                    "spawn": None,
                    "fire_cells": [],
                    "ice_cells": [],
                    "fire_healing_area": None,
                    "ice_healing_area": None,
                    "pos": [1, 0]
                },
                {
                    "spawn": None,
                    "fire_cells": [],
                    "ice_cells": [],
                    "fire_healing_area": None,
                    "ice_healing_area": {
                        "positions": [[0, 0],[0, 1],[0, 2],[1, 0],[1, 1],[1, 2],[2, 0],[2, 1],[2, 2]],
                        "duration": 100,
                        "healing_rate": 3,
                        "affected_cell_type": "IceCell"
                    },
                    "pos": [1, 1]
                }
            ]
        ]
    }

def test_create_from_dict(board_dict):
    board = Board.create_from_dict(board_dict)
    print(str(board))
    assert board.rows == board_dict['rows']
    assert board.columns == board_dict['columns']
    for i in range(board.rows):
        for j in range(board.columns):
            box = board.board[i][j]
            dict_box = board_dict['board'][i][j]
            assert box.spawn == IceSpawn.create_from_dict(dict_box['spawn']) or box.spawn == FireSpawn.create_from_dict(dict_box['spawn'])
            assert box.fire_cells == [FireCell.create_from_dict(cell_dict) for cell_dict in dict_box['fire_cells']]
            assert box.ice_cells == [IceCell.create_from_dict(cell_dict) for cell_dict in dict_box['ice_cells']]
            assert box.fire_healing_area == HealingArea.create_from_dict(dict_box['fire_healing_area'])
            assert box.ice_healing_area == HealingArea.create_from_dict(dict_box['ice_healing_area'])
            #assert box.pos == dict_box['pos']
            assert box.pos == tuple(dict_box['pos'])


def test_create_from_dict2(board_dict):
    # Create the board from the dictionary
    board = Board.create_from_dict(board_dict)

    # Manually create a new board with the same data
    manual_board = Board(board_dict['rows'], board_dict['columns'])
    for i in range(board_dict['rows']):
        for j in range(board_dict['columns']):
            dict_box = board_dict['board'][i][j]
            box = Box()
            box.spawn = IceSpawn.create_from_dict(dict_box['spawn']) if dict_box['spawn'] and dict_box['spawn']['type'] == 'IceSpawn' else FireSpawn.create_from_dict(dict_box['spawn'])
            box.fire_cells = [FireCell.create_from_dict(cell_dict) for cell_dict in dict_box['fire_cells']]
            box.ice_cells = [IceCell.create_from_dict(cell_dict) for cell_dict in dict_box['ice_cells']]
            box.fire_healing_area = HealingArea.create_from_dict(dict_box['fire_healing_area'])
            box.ice_healing_area = HealingArea.create_from_dict(dict_box['ice_healing_area'])
            #box.pos = dict_box['pos']
            box.pos = tuple(dict_box['pos'])

            manual_board.board[i][j] = box
    assert board == manual_board

def test_add_cell(board):
    cell = FireCell()
    board.add_cell(1, 0, cell)
    assert cell in board.get_cells(1,0)

def test_remove_cell(board):
    cell = FireCell()
    board.add_cell(1, 0, cell)
    assert cell in board.get_cells(1,0)
    board.remove_cell(1, 0, cell)
    assert cell not in board.get_cells(1, 0)

def test_get_box(board):
    cell1 = FireCell()
    cell2 = IceCell()
    print(str(board))
    board.add_cell(2, 0, cell1)
    board.add_cell(2, 0, cell2)
    cells = board.get_cells(2, 0)
    assert len(cells) == 2
    assert cell1 in cells
    assert cell2 in cells

def test_to_string():
    board = Board(8,8)
    print(str(board))
    board.create_spawn(1,1, IceSpawn)
    board.create_spawn(6,6, FireSpawn)
    board.create_healing_area(4,4, IceCell)
    board.add_cell(5,5,IceCell())
    string_board = str(board)
    assert string_board == 'IS|IS|IS| | | | | \n'\
                           'IS|IS|IS| | | | | \n'\
                           'IS|IS|IS| | | | | \n'\
                           ' | | |IH|IH|IH| | \n'\
                           ' | | |IH|IH|IH| | \n'\
                           ' | | |IH|IH|FS,IH,I|FS|FS\n'\
                           ' | | | | |FS|FS|FS\n'\
                           ' | | | | |FS|FS|FS'\

# def test_get_pos(board):s
#     cell1 = FireCell()
#     cell2 = IceCell()
#     board.add_cell(0, 0, cell1)
#     board.add_cell(1, 1, cell2)

#     assert board.get_pos(cell1) == (0, 0)
#     assert board.get_pos(cell2) == (1, 1)

#     cell3 = FireCell()
#     assert board.get_pos(cell3) is None


def test_create_spawn(board):
    board.create_spawn(1, 1, IceSpawn)
    adjacent_positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    assert board.get_box(1, 1).get_spawn() is not None
    assert isinstance(board.get_box(1,1).get_spawn(), IceSpawn)

    for position in adjacent_positions:
        assert board.get_box(*position).get_spawn() is not None
        assert isinstance(board.get_box(*position).get_spawn(), IceSpawn)

def create_test_box():
    spawn = IceSpawn(positions=[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
    fire_cells = [FireCell(), FireCell()]
    ice_cells = [IceCell(), IceCell()]
    fire_healing_area = HealingArea(positions=[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)], affected_cell_type=FireCell)
    ice_healing_area = None
    pos = (0, 0)
    return Box(spawn, fire_cells, ice_cells, fire_healing_area, ice_healing_area, pos)

# Ahora, la prueba en pytest para comparar dos tableros de 2x2
def test_board_equality():
    # Inicializa dos tableros con los mismos Boxes
    box1 = create_test_box()
    box2 = create_test_box()

    board1 = Board(2, 2, [[box1, box1], [box1, box1]])
    board2 = Board(2, 2, [[box2, box2], [box2, box2]])

    # Compara los tableros
    assert board1 == board2