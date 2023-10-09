import pytest

from logic.board import Board
from logic.cell import IceCell, FireCell, DeadCell, Level

@pytest.fixture
def board():
    return Board(2, 2)

def test_add_cell(board):
    cell = FireCell()
    board.add_cell(1, 0, cell)
    assert cell in board.get_cells(1, 0)

def test_add_cell_by_tuple(board):
    cell = FireCell()
    position = (1, 0)
    board.add_cell_by_tuple(position, cell)
    assert cell in board.get_cells(*position)

def test_remove_cell(board):
    cell = FireCell()
    board.add_cell(1, 0, cell)
    assert cell in board.get_cells(1, 0)
    board.remove_cell(1, 0, cell)
    assert cell not in board.get_cells(1, 0)

def test_get_cells(board):
    cell1 = FireCell()
    cell2 = IceCell()
    board.add_cell(1, 0, cell1)
    board.add_cell(1, 0, cell2)
    cells = board.get_cells(1, 0)
    assert len(cells) == 2
    assert cell1 in cells
    assert cell2 in cells

def test_get_pos(board):
    cell1 = FireCell()
    cell2 = IceCell()
    board.add_cell(0, 0, cell1)
    board.add_cell(1, 1, cell2)

    assert board.get_pos(cell1) == (0, 0)
    assert board.get_pos(cell2) == (1, 1)

    cell3 = FireCell()
    assert board.get_pos(cell3) is None


###Tests for convert_two_cells_to_dead_cell:

def test_convert_two_cells_to_dead_cell(board):
    row, column = 0, 0
    cell1 = FireCell()
    cell2 = IceCell()
    board.add_cell(row, column, cell1)
    board.add_cell(row, column, cell2)
    board.convert_two_cells_to_dead_cell(row, column, cell1, cell2)
    assert len(board.get_cells(row, column)) == 1
    assert isinstance(board.get_cells(row, column)[0], DeadCell)


def test_convert_two_cells_to_dead_cell_invalid_position(board):
    row, column = 3, 3
    cell1 = FireCell()
    cell2 = IceCell()
    with pytest.raises(ValueError):
        board.convert_two_cells_to_dead_cell(row, column, cell1, cell2)

def test_convert_two_cells_to_dead_cell_cell_not_in_position(board):
    row, column = 0, 0
    cell1 = FireCell()
    cell2 = IceCell()
    board.add_cell(row, column, cell1)
    with pytest.raises(ValueError):
        board.convert_two_cells_to_dead_cell(row, column, cell1, cell2)
    
## TEST Fusion of Board
def test_fusion_board(board):
    pos = (1,1)
    board.add_cell(pos[0], pos[1], FireCell(level=Level.LEVEL_2, life=36, position=pos, board=board))
    board.add_cell(pos[0], pos[1], FireCell(level=Level.LEVEL_1, life=16, position=pos, board=board))
    board.add_cell(pos[0], pos[1], FireCell(level=Level.LEVEL_1, life=7, position=pos, board=board))
    board.add_cell(pos[0], pos[1], IceCell(level=Level.LEVEL_1, life=2, position=pos, board=board))
    board.add_cell(pos[0], pos[1], IceCell(level=Level.LEVEL_1, life=12, position=pos, board=board))
    board.fusion(pos)
    cells_in_pos = board.get_cells(pos[0], pos[1])
    assert len(cells_in_pos) == 2
    assert isinstance(cells_in_pos[0], FireCell)
    assert isinstance(cells_in_pos[1], IceCell)
    assert cells_in_pos[0].life == 60
    assert cells_in_pos[0].level == Level.LEVEL_3
    assert cells_in_pos[1].life == 40
    assert cells_in_pos[1].level == Level.LEVEL_2

    
    
    
