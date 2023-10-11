from behave import given, when, then
from logic.board import Board
from logic.cell import Cell, IceCell, FireCell, DeadCell, Level

@given(u'I have a level {level:d} ice cell at position ({rows:d}, {columns:d}), with {life:d} health points')
def step_impl(context, rows, columns, level, life):
    context.state.board = Board(50,50)
    context.state.board.add_cell(rows, columns, IceCell(level=Level(level), life = life))

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

@when(u'I try to move the level {level:d} ice cell to position ({rows:d}, {columns:d}) with {life:d} health points')
def step_impl(context, rows, columns, level, life):
    context.state.board.add_cell(rows, columns, IceCell(level = Level(level), life = life))
    context.state.board.remove_cell(rows - 1, columns, context.state.board.get_cells(rows - 1, columns)[0])

@when(u'I try to move the level {level:d} fire cell to position ({rows:d}, {columns:d}) with {life:d} health points')
def step_impl(context, rows, columns, level, life):
    context.state.board.add_cell(rows, columns, FireCell(level = Level(level), life = life))
    context.state.board.remove_cell(rows - 1, columns, context.state.board.get_cells(rows - 1, columns)[0])
    '''if rows > 0 and rows < 50 and columns > 0 and columns < 50: 
        context.state.board.remove_cell(rows - 1, columns, context.state.board.get_cells(rows - 1, columns)[0])
    else:
        raise AssertionError('Range error')'''

@then(u'the ice cell moves successfully to position ({rows:d}, {columns:d})')
def step_impl(context, rows, columns):
    assert len(context.state.board.get_cells(rows, columns)) == 1 

@then(u'the fire cell moves successfully to position ({rows:d}, {columns:d})')
def step_impl(context, rows, columns):
    assert len(context.state.board.get_cells(rows, columns)) == 1 

@then(u'both cells cannot merge, and coexist at position ({rows:d}, {columns:d})')
def step_impl(context, rows, columns):
    assert len(context.state.board.get_cells(rows, columns)) == 2
