from logic.cell import IceCell, FireCell, DeadCell, Cell, Level
from logic.board import Board
##########Scenario: Fusion Two Level 1 Ice Cells
@given(u'I have a level 1 ice cell at position ({row:d},{column:d}) with 5 health points')
def step_impl(context, row, column):
    context.state.board = Board(50, 50)  

    ice_cell = IceCell(level=Level.LEVEL_1, board=context.state.board, life=5, position=(row,column))
    
    context.state.board.add_cell(row, column, ice_cell)

@given(u'another level 1 ice cell at position ({row:d},{column:d}) with 10 health points')
def step_impl(context, row, column):

    ice_cell = IceCell(level=Level.LEVEL_1, board=context.state.board, life=10, position=(row,column))
    
    context.state.board.add_cell(row, column, ice_cell)

@when(u'fusion start at position ({row:d},{column:d})')
def step_impl(context, row, column):
    ice_cell = context.state.board.get_cells(row, column)[0]
    ice_cell2 = context.state.board.get_cells(row, column)[1]
    ice_cell.fusion_cell(ice_cell2)

@then(u'a level 2 ice cell is created at position ({row:d},{column:d}) with 40 health points and the level 1 ice cells at ({row:d},{column:d}) disappears from the battlefield')
def step_impl(context, row, column):
    assert len(context.state.board.get_cells(row, column)) == 1
    assert isinstance(context.state.board.get_cells(row, column)[0], IceCell)
    assert context.state.board.get_cells(row, column)[0].get_life() == 40
    assert context.state.board.get_cells(row, column)[0].get_level() == 2