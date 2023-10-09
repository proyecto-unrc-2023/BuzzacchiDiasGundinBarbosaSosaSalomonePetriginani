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

    
def test_fusion_in_all_board(board):
    pos0 = (0,0)
    board.add_cell(pos0[0], pos0[1], IceCell(level=Level.LEVEL_2, life=36, position=pos0, board=board))
    board.add_cell(pos0[0], pos0[1], IceCell(level=Level.LEVEL_2, life=30, position=pos0, board=board))

    pos1 = (0,1)
    board.add_cell(pos1[0], pos1[1], IceCell(level=Level.LEVEL_1, life=15, position=pos1, board=board))
    board.add_cell(pos1[0], pos1[1], IceCell(level=Level.LEVEL_1, life=2, position=pos1, board=board))

    pos2 = (1,0)
    board.add_cell(pos2[0], pos2[1], FireCell(level=Level.LEVEL_3, life=48, position=pos2, board=board))
    board.add_cell(pos2[0], pos2[1], IceCell(level=Level.LEVEL_1, life=15, position=pos2, board=board))
    
    pos3 = (1,1)
    board.add_cell(pos3[0], pos3[1], FireCell(level=Level.LEVEL_3, life=50, position=pos3, board=board))
    board.add_cell(pos3[0], pos3[1], FireCell(level=Level.LEVEL_2, life=29, position=pos3, board=board))

    board.execute_fusions_in_all_positions()

    cells_in_pos_00 = board.get_cells(0, 0)
    cells_in_pos_01 = board.get_cells(0, 1)
    cells_in_pos_10 = board.get_cells(1, 0)
    cells_in_pos_11 = board.get_cells(1, 1)

    # Comprueba la fusión en (0, 0)
    assert len(cells_in_pos_00) == 1
    assert isinstance(cells_in_pos_00[0], IceCell)
    assert cells_in_pos_00[0].life == 60
    assert cells_in_pos_00[0].level == Level.LEVEL_3

    # Comprueba la fusión en (0, 1)
    assert len(cells_in_pos_01) == 1
    assert isinstance(cells_in_pos_01[0], IceCell)
    assert cells_in_pos_01[0].life == 40
    assert cells_in_pos_01[0].level == Level.LEVEL_2

    # Comprueba la fusión en (1, 0)
    assert len(cells_in_pos_10) == 2
    assert isinstance(cells_in_pos_10[0], FireCell)
    assert isinstance(cells_in_pos_10[1], IceCell)
    assert cells_in_pos_10[0].life == 48
    assert cells_in_pos_10[0].level == Level.LEVEL_3
    assert cells_in_pos_10[1].life == 15
    assert cells_in_pos_10[1].level == Level.LEVEL_1

    # Comprueba que no hubo fusión en (1, 1)
    assert len(cells_in_pos_11) == 2
    assert isinstance(cells_in_pos_11[0], FireCell)
    assert isinstance(cells_in_pos_11[1], FireCell)
    assert cells_in_pos_11[0].life == 50
    assert cells_in_pos_11[0].level == Level.LEVEL_3
    assert cells_in_pos_11[1].life == 29
    assert cells_in_pos_11[1].level == Level.LEVEL_2
    
    
