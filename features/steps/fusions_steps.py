from behave import given, when, then
from logic.cell import IceCell, FireCell, DeadCell, Cell, Level
from logic.board import Board

@given(u'a level {level:d} {team} cell at position ({row:d}, {column:d}) with {life:d} health points')
def step_imp(context, row, column, level, life, team):
    context.GameController.create_cell(row, column, team, level, life)
    
@when(u'fusion start at position ({row:d}, {column:d})')
def step_impl(context, row, column):
    print(str(context.GameController.get_board()))
    context.GameController.execute_fusion()

@then(u'a level {level_c1:d} Ice cell is created at position ({row:d}, {column:d}) with {life:d} health points and the level {level_c2:d} Ice cells at ({row:d}, {column:d}) disappears from the battlefield')
def step_impl(context, row, column, life, level_c1, level_c2):
    print(str(context.GameController.get_board()))
    assert len(context.GameController.get_cells(row, column)) == 1
    assert isinstance(context.GameController.get_cells(row, column)[0], IceCell)
    assert context.GameController.get_cells(row, column)[0].get_life() == life
    assert context.GameController.get_cells(row, column)[0].get_level() == level_c1

@then(u'a level {level_c1:d} Fire cell is created at position ({row:d}, {column:d}) with {life:d} health points and the level {level_c2:d} Fire cells at ({row:d}, {column:d}) disappears from the battlefield')
def step_impl(context, row, column, life, level_c1, level_c2):
    assert len(context.GameController.get_cells(row, column)) == 1
    assert isinstance(context.GameController.get_cells(row, column)[0], FireCell)
    assert context.GameController.get_cells(row, column)[0].get_life() == life
    assert context.GameController.get_cells(row, column)[0].get_level() == level_c1

@then(u'the Ice cells cannot merge, and both coexist two cells level {level_c1:d} with {life_c1:d} health points and other cell level {level_c2:d} with {life_c2:d} health points at position ({row:d}, {column:d})')
def step_impl(context, row, column, level_c1, level_c2, life_c1, life_c2):
    assert len(context.GameController.get_cells(row, column)) == 2
    assert isinstance(context.GameController.get_cells(row,column)[0], IceCell)
    assert isinstance(context.GameController.get_cells(row,column)[1], IceCell)
    assert context.GameController.get_cells(row,column)[0].get_life() == life_c1
    assert context.GameController.get_cells(row,column)[0].get_level() == level_c1
    assert context.GameController.get_cells(row,column)[1].get_life() == life_c2
    assert context.GameController.get_cells(row,column)[1].get_level() == level_c2
    
@then(u'the Fire cells cannot merge, and both coexist two cells level {level_c1:d} with {life_c1:d} health points and other cell level {level_c2:d} with {life_c2:d} health points at position ({row:d}, {column:d})')
def step_impl(context, row, column, level_c1, level_c2, life_c1, life_c2):
    assert len(context.GameController.get_cells(row, column)) == 2
    assert isinstance(context.GameController.get_cells(row,column)[0], FireCell)
    assert isinstance(context.GameController.get_cells(row,column)[1], FireCell)
    assert context.GameController.get_cells(row,column)[0].get_life() == life_c1
    assert context.GameController.get_cells(row,column)[0].get_level() == level_c1
    assert context.GameController.get_cells(row,column)[1].get_life() == life_c2
    assert context.GameController.get_cells(row,column)[1].get_level() == level_c2

@then(u'a level {level_c1:d} Ice cell is created at position ({row:d}, {column:d}) with {life:d} health points and only one level {level_c2:d} Ice cell at ({row:d}, {column:d}) with {life_c2:d} health points disappears from the battlefield')
def step_impl(context, row, column, life, life_c2, level_c1, level_c2):
    assert len(context.GameController.get_cells(row, column)) == 2
    assert isinstance(context.GameController.get_cells(row,column)[0], IceCell)
    assert isinstance(context.GameController.get_cells(row,column)[1], IceCell)
    assert context.GameController.get_cells(row,column)[0].get_life() == life
    assert context.GameController.get_cells(row,column)[0].get_level() == level_c1
    assert context.GameController.get_cells(row,column)[1].get_life() == life_c2
    assert context.GameController.get_cells(row,column)[1].get_level() == level_c2

@then(u'a level {level:d} Fire cells is created at position ({row:d}, {column:d}) with {life:d} health points and all level 1 Fire cells at ({row:d}, {column:d}) disappears from the battlefield')
def step_impl(context, row, column, life, level):
    assert len(context.GameController.get_cells(row, column)) == 1
    assert isinstance(context.GameController.get_cells(row,column)[0], FireCell)
    assert context.GameController.get_cells(row,column)[0].get_life() == life
    assert context.GameController.get_cells(row,column)[0].get_level() == level
