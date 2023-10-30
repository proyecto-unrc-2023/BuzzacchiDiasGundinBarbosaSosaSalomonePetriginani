import pytest

from logic.board import Board
from logic.cell import IceCell, FireCell
from logic.spawn import IceSpawn, FireSpawn

@pytest.fixture
def board():
    return Board(10, 10)

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
    board.add_cell(1, 0, cell1)
    board.add_cell(1, 0, cell2)
    cells = board.get_cells(1, 0)
    assert len(cells) == 2
    assert cell1 in cells
    assert cell2 in cells

def test_to_string():
    board = Board(8,8)
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