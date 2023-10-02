from logic.board import Board
from logic.cell import Cell, IceCell, FireCell, DeadCell

###Scenario: Move level 1 cell to an empty adjacent cell
@given(u'I have a level {level:d} cell at position ({rows:d}, {columns:d}), with {life:d} health points')
def step_impl(context, rows, columns, level, life):
    context.state.board = Board(50,50)
    context.state.board.add_cell(rows, columns, IceCell(Cell(level = level, life = life)))

@given(u'the adjacent cell at position ({rows:d}, {columns:d}) is empty')
def step_impl(context, rows, columns):
    if isinstance(context.state.board.get_cells(rows, columns).__str__(), DeadCell().__str__()):
      pass
    else:
      raise AssertionError('Cell position is not empty')

@when(u'I try to move the cell to position ({x:d}, {y:d})')
def step_impl(context, x, y):
    position = (x, y)
    context.state.cell.set_position(position)

@then(u'the cell moves successfully to position ({x:d}, {y:d})')
def step_impl(context, x, y):
     context

###Scenario: Attempt to move level 1 cell to a cell occupied by another level 1 cell

@given(u'I have a level {level:d} ice cell with life {life:d} at position {position:d}')
def step_impl(context, position, level, life):
    context.state.Board(50,50)
    context.state.Board.add_cell_by_tuple(position, IceCell(level = level, life = life))

@given(u'another level {level:d} ice cell whit life {life:d} at position {position:d}')
def step_impl(context, position, level, life):
    context.state.Board(50,50)
    context.state.Board.add_cell_by_tuple(position, IceCell(level = level, life = life))

@when(u'I try to move the level {level:d} ice cell to position {position:d}')
def step_impl(context, position, level):
    context.state.IceCell.set_position(position)

@then(u'both cells coexist in cell ({x:d}, {y:d})')
def step_impl(context, x, y):
    assert context.state.len(Board.get_cells(x, y)) == 2