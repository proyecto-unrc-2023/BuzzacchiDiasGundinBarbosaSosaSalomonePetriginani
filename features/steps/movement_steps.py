from behave import given, when, then
from logic.board import Board
from logic.cell import Cell, IceCell, FireCell, DeadCell, Level

###Scenario: Move level 1 ice cell to an empty adjacent cell
@given(u'I have a level {level:d} ice cell at position ({rows:d}, {columns:d}), with {life:d} health points')
def step_impl(context, rows, columns, level, life):
    context.state.board = Board(50,50)
    context.state.board.add_cell(rows, columns, IceCell(level=Level(level), life = life))

@given(u'the adjacent cell at position ({rows:d}, {columns:d}) is empty')
def step_impl(context, rows, columns):
    if len(context.state.board.get_cells(rows, columns)) == 0:
      pass
    else:
      raise AssertionError('Cell position is not empty')

@when(u'I try to move the level {level:d} ice cell to position ({x:d}, {y:d})')
def step_impl(context, x, y, level):
    context.state.board.add_cell(x, y, IceCell(level = Level(level), life = 14))
    context.state.board.remove_cell(x - 1, y, context.state.board.get_cells(x - 1, y)[0])

@then(u'the ice cell moves successfully to position ({x:d}, {y:d})')
def step_impl(context, x, y):
    assert len(context.state.board.get_cells(x, y)) == 1 


###Scenario: Move level 1 fire cell to an empty adjacent cell
@given(u'I have a level {level:d} fire cell at position ({rows:d}, {columns:d}), with {life:d} health points')
def step_impl(context, rows, columns, level, life):
    context.state.board = Board(50,50)
    context.state.board.add_cell(rows, columns, FireCell(level = Level(level), life = life))

@given(u'the adjacent cell at position ({rows:d}, {columns:d}) is empty')
def step_impl(context, rows, columns):
    if len(context.state.board.get_cells(rows, columns)) == 0:
      pass
    else:
      raise AssertionError('Cell position is not empty')

@when(u'I try to move the level {level:d} fire cell to position ({x:d}, {y:d})')
def step_impl(context, x, y, level):
    context.state.board.add_cell(x, y, FireCell(level = Level(level), life = 14))
    context.state.board.remove_cell(x - 1, y, context.state.board.get_cells(x - 1, y)[0])

@then(u'the fire cell moves successfully to position ({x:d}, {y:d})')
def step_impl(context, x, y):
    assert len(context.state.board.get_cells(x, y)) == 1 


###Scenario: Attempt to move level 1 ice cell to an adjacent cell occupied by a level 3 cell
@given(u'I have a level {level:d} ice cell with life {life:d} at position ({row:d}, {column:d})')
def step_impl(context, row, column, level, life):
    context.state.board = Board(50,50)
    context.state.board.add_cell(row, column, IceCell(level = Level(level), life = life))

@given(u'another level {level:d} ice cell with life {life:d} at position ({row:d}, {column:d})')
def step_impl(context, level, life, row, column):
    context.state.board.add_cell(row, column, IceCell(level = Level(level), life = life))

@when(u'I try to move the level {level:d} ice cell to position ({row:d}, {column:d})')
def step_impl(context, row, column, level):
    context.state.board.add_cell(row, column, IceCell(level = Level(level)))
    context.state.board.remove_cell(row - 1, column, context.state.board.get_cells(row - 1, column)[0])

@then(u'both cells coexist in cell ({x:d}, {y:d})')
def step_impl(context, x, y):
    assert len(context.state.board.get_cells(x, y)) == 2


###Scenario: Attempt to move level 1 fire cell to a cell occupied by another level 3 cell
@given(u'I have a level {level:d} fire cell with life {life:d} at position ({row:d}, {column:d})')
def step_impl(context, row, column, level, life):
    context.state.board = Board(50,50)
    context.state.board.add_cell(row, column, FireCell(level = Level(level), life = life))

@given(u'another level {level:d} fire cell with life {life:d} at position ({row:d}, {column:d})')
def step_impl(context, level, life, row, column):
    context.state.board.add_cell(row, column, FireCell(level = Level(level), life = life))

@when(u'I try to move the level {level:d} fire cell to position ({row:d}, {column:d})')
def step_impl(context, row, column, level):
    context.state.board.add_cell(row, column, FireCell(level = Level(level)))
    context.state.board.remove_cell(row - 1, column, context.state.board.get_cells(row - 1, column)[0])

@then(u'both cells coexist in cell ({x:d}, {y:d})')
def step_impl(context, x, y):
    assert len(context.state.board.get_cells(x, y)) == 2


###Scenario: Attempt to move level 2 ice cell to an adjacent cell occupied by a level 1 ice cell
@given(u'I have a level {level:d} ice cell with life {life:d} at position ({row:d}, {column:d})')
def step_impl(context, row, column, level, life):
    context.state.board = Board(50,50)
    context.state.board.add_cell(row, column, IceCell(level = Level(level), life = life))

@given(u'a level {level:d} ice cell with life {life:d} at position ({row:d}, {column:d})')
def step_impl(context, row, column, level, life):
    context.state.board.add_cell(row, column, IceCell(level = Level(level), life = life))

@when(u'I try to move the level {level:d} ice cell to position ({row:d}, {column:d}) with {life:d} health points')
def step_impl(context, row, column, level, life):
    context.state.board.add_cell(row, column, IceCell(level = Level(level), life = life))
    context.state.board.remove_cell(row - 1, column, context.state.board.get_cells(row - 1, column)[0])

@then(u'both cells cannot merge, and coexist at position ({x:d}, {y:d})')
def step_impl(context, x, y):
    assert len(context.state.board.get_cells(x, y)) == 2

###Scenario: Attempt to move level 2 fire cell to an adjacent cell occupied by a level 1 fire cell
@given(u'I have a level {level:d} fire cell with life {life:d} at position ({row:d}, {column:d})')
def step_impl(context, row, column, level, life):
    context.state.board = Board(50,50)
    context.state.board.add_cell(row, column, FireCell(level = Level(level), life = life))

@given(u'a level {level:d} fire cell with life {life:d} at position ({row:d}, {column:d})')
def step_impl(context, row, column, level, life):
    context.state.board.add_cell(row, column, FireCell(level = Level(level), life = life))

@when(u'I try to move the level {level:d} fire cell to position ({row:d}, {column:d}) with {life:d} health points')
def step_impl(context, row, column, level, life):
    context.state.board.add_cell(row, column, FireCell(level = Level(level), life = life))
    context.state.board.remove_cell(row - 1, column, context.state.board.get_cells(row - 1, column)[0])
    #assert FireCell.get_level() == Level.LEVEL_2

@then(u'both cells cannot merge, and coexist at position ({row:d}, {column:d})')
def step_impl(context, row, column):
    assert len(context.state.board.get_cells(row, column)) == 2