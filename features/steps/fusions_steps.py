from logic.cell import IceCell, FireCell, DeadCell, Cell, Level
from logic.board import Board
##########Scenario: Fusion Two Level 1 Ice Cells
@given(u'I have a level 1 ice cell at position ({row:d},{column:d}) with {life:d} health points')
def step_impl(context, row, column, life):
    context.state.board = Board(50, 50)  
    ice_cell = IceCell(level=Level.LEVEL_1, board=context.state.board, life=life, position=(row,column))
    context.state.board.add_cell(row, column, ice_cell)

@given(u'another level 1 ice cell at position ({row:d},{column:d}) with {life:d} health points')
def step_impl(context, row, column, life):
    ice_cell = IceCell(level=Level.LEVEL_1, board=context.state.board, life=life, position=(row,column))
    context.state.board.add_cell(row, column, ice_cell)

@when(u'fusion start at position ({row:d},{column:d})')
def step_impl(context, row, column):
    ice_cell = context.state.board.get_cells(row, column)[0]
    ice_cell2 = context.state.board.get_cells(row, column)[1]
    ice_cell.fusion_cell(ice_cell2)

@then(u'a level 2 ice cell is created at position ({row:d},{column:d}) with {life:d} health points and the level 1 ice cells at ({row:d},{column:d}) disappears from the battlefield')
def step_impl(context, row, column, life):
    assert len(context.state.board.get_cells(row, column)) == 1
    assert isinstance(context.state.board.get_cells(row, column)[0], IceCell)
    assert context.state.board.get_cells(row, column)[0].get_life() == life
    assert context.state.board.get_cells(row, column)[0].get_level() == 2
    
##########Scenario: Fusion Two Level 2 Fire Cells
@given(u'I have a level 2 fire cell at position ({row:d},{column:d}) with {life:d} health points')
def step_impl(context, row, column, life):
    context.state.board = Board(50, 50)
    fire_cell = FireCell(level=Level.LEVEL_2, board=context.state.board, life=life, position=(row,column))
    context.state.board.add_cell(row, column, fire_cell)
    
@given(u'another level 2 fire cell at position ({row:d},{column:d}) with {life:d} health points')
def step_impl(context, row, column, life):
    fire_cell = FireCell(level=Level.LEVEL_2, board=context.state.board, life=life, position=(row,column))
    context.state.board.add_cell(row, column, fire_cell)
    
@when(u'fusion start at position ({row:d},{column:d})')
def step_impl(context, row, column):
    fire_cell = context.state.board.get_cells(row, column)[0]
    fire_cell2 = context.state.board.get_cells(row,column)[1]
    fire_cell.fusion_cell(fire_cell2)

@then(u'a level 3 fire cell is created at position ({row:d},{column:d}) with {life:d} health points and the level 2 fire cells at ({row:d},{column:d}) disappears from the battlefield')
def step_impl(context, row, column, life):
    assert len(context.state.board.get_cells(row, column)) == 1
    assert isinstance(context.state.board.get_cells(row,column)[0], FireCell)
    assert context.state.board.get_cells(row,column)[0].get_life() == life
    assert context.state.board.get_cells(row,column)[0].get_level() == 3

############ Scenario: Attempt to merge two level 3 ice cells
@given(u'I have a level 3 ice cell at position ({row:d},{column:d})')
def step_impl(context, row, column):
    context.state.board = Board(50, 50)
    ice_cell = IceCell(level=Level.LEVEL_3, board=context.state.board, life=53, position=(row,column))
    context.state.board.add_cell(row, column, ice_cell)
    
@given(u'another level 3 ice cell at position ({row:d},{column:d})')
def step_impl(context, row, column):
    ice_cell = IceCell(level=Level.LEVEL_3, board=context.state.board, life=45, position=(row,column))
    context.state.board.add_cell(row, column, ice_cell)
    
@when(u'fusion start at position ({row:d},{column:d})')
def step_impl(context, row, column):
    ice_cell = context.state.board.get_cells(row, column)[0]
    ice_cell2 = context.state.board.get_cells(row,column)[1]
    ice_cell.fusion_cell(ice_cell2)
    
@then(u'the cells cannot merge, and both coexist at position ({row:d},{column:d})')
def step_impl(context, row, column):
    assert len(context.state.board.get_cells(row, column)) == 2
    assert isinstance(context.state.board.get_cells(row,column)[0], IceCell)
    assert isinstance(context.state.board.get_cells(row,column)[1], IceCell)
    assert context.state.board.get_cells(row,column)[0].get_life() == 53
    assert context.state.board.get_cells(row,column)[0].get_level() == 3
    assert context.state.board.get_cells(row,column)[1].get_life() == 45
    assert context.state.board.get_cells(row,column)[1].get_level() == 3
    
######## Scenario: Attempt to merge a level 2 fire cell with a level 3 fire cell
@given(u'I have a level 2 fire cell at position ({row:d},{column:d})')
def step_impl(context, row, column):
    context.state.board = Board(50, 50)
    fire_cell = FireCell(level=Level.LEVEL_2, board=context.state.board, life=21, position=(row,column))
    context.state.board.add_cell(row, column, fire_cell)
    
@given(u'a level 3 fire cell at position ({row:d},{column:d})')
def step_impl(context, row, column):
    fire_cell = FireCell(level=Level.LEVEL_3, board=context.state.board, life=41, position=(row,column))
    context.state.board.add_cell(row, column, fire_cell)
    
@when(u'fusion start at position ({row:d},{column:d})')
def step_impl(context, row, column):
    fire_cell = context.state.board.get_cells(row, column)[0]
    fire_cell2 = context.state.board.get_cells(row,column)[1]
    fire_cell.fusion_cell(fire_cell2)
    
@then(u'the cells cannot merge and both coexist in ({row:d},{column:d})')
def step_impl(context, row, column):
    assert len(context.state.board.get_cells(row, column)) == 2
    assert isinstance(context.state.board.get_cells(row,column)[0], FireCell)
    assert isinstance(context.state.board.get_cells(row,column)[1], FireCell)
    assert context.state.board.get_cells(row,column)[0].get_life() == 21
    assert context.state.board.get_cells(row,column)[0].get_level() == 2
    assert context.state.board.get_cells(row,column)[1].get_life() == 41
    assert context.state.board.get_cells(row,column)[1].get_level() == 3