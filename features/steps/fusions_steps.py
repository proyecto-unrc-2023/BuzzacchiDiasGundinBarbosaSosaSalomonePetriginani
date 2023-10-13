from behave import given, when, then
from logic.cell import IceCell, FireCell, DeadCell, Cell, Level
from logic.board import Board

@when(u'fusion start at position ({row:d}, {column:d})')
def step_impl(context, row, column):
    pos = (row, column)
    context.state.board.fusion(pos)

@then(u'a level {level_fusion:d} ice cell is created at position ({row:d}, {column:d}) with {life:d} health points and the level {level:d} ice cells at ({row:d}, {column:d}) disappears from the battlefield')
def step_impl(context, row, column, life, level_fusion):
    assert len(context.state.board.get_cells(row, column)) == 1
    assert isinstance(context.state.board.get_cells(row, column)[0], IceCell)
    assert context.state.board.get_cells(row, column)[0].get_life() == life
    assert context.state.board.get_cells(row, column)[0].get_level() == level_fusion
    
@then(u'a level {level_fusion:d} fire cell is created at position ({row:d},{column:d}) with {life:d} health points and the level {level:d} fire cells at ({row:d},{column:d}) disappears from the battlefield')
def step_impl(context, row, column, life, level_fusion):
    assert len(context.state.board.get_cells(row, column)) == 1
    assert isinstance(context.state.board.get_cells(row,column)[0], FireCell)
    assert context.state.board.get_cells(row,column)[0].get_life() == life
    assert context.state.board.get_cells(row,column)[0].get_level() == level_fusion

@then(u'the cells cannot merge, and both coexist two cells level {level_c1:d} with {life_c1:d} health points and other cell {level_c2:d} with {life_c2:d} health points at position ({row:d}, {column:d})')
def step_impl(context, row, column, level_c1, level_c2, life_c1, life_c2):
    assert len(context.state.board.get_cells(row, column)) == 2
    assert isinstance(context.state.board.get_cells(row,column)[0], IceCell)
    assert isinstance(context.state.board.get_cells(row,column)[1], IceCell)
    assert context.state.board.get_cells(row,column)[0].get_life() == life_c1
    assert context.state.board.get_cells(row,column)[0].get_level() == level_c1
    assert context.state.board.get_cells(row,column)[1].get_life() == life_c2
    assert context.state.board.get_cells(row,column)[1].get_level() == level_c2

@then(u'a level {level_c1:d} ice cell is created at position ({row:d}, {column:d}) with {life:d} health points and only one level {level_c2:d} ice cell at ({row:d}, {column:d}) with {life_c2:d} health points disappears from the battlefield')
def step_impl(context, row, column, life, life_c2, level_c1, level_c2):
    assert len(context.state.board.get_cells(row, column)) == 2
    assert isinstance(context.state.board.get_cells(row,column)[0], IceCell)
    assert isinstance(context.state.board.get_cells(row,column)[1], IceCell)
    assert context.state.board.get_cells(row,column)[0].get_life() == life
    assert context.state.board.get_cells(row,column)[0].get_level() == level_c1
    assert context.state.board.get_cells(row,column)[1].get_life() == life_c2
    assert context.state.board.get_cells(row,column)[1].get_level() == level_c2

@then(u'a level {level:d} fire cells is created at position ({row:d}, {column:d}) with {life:d} health points and all level 1 fire cells at ({row:d}, {column:d}) disappears from the battlefield')
def step_impl(context, row, column, life, level):
    assert len(context.state.board.get_cells(row, column)) == 1
    assert isinstance(context.state.board.get_cells(row,column)[0], FireCell)
    assert context.state.board.get_cells(row,column)[0].get_life() == life
    assert context.state.board.get_cells(row,column)[0].get_level() == level
