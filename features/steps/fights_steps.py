from logic.cell import IceCell, FireCell, DeadCell, Cell
from logic.board import Board


##########Scenario: Two level 1 cells fights
@given(u'there are two cells, one IceCell with 8 life points and one FireCell with 5 life points level 1 in position ({row:d},{column:d})')
def step_impl(context, row, column):
    context.state.board = Board(50, 50)  

    ice_cell = IceCell(level=1, board=context.state.board, life=8, position=(row,column))
    fire_cell = FireCell(level=1, board=context.state.board, life=5, position=(row,column))
    
    context.state.board.add_cell(row, column, ice_cell)
    context.state.board.add_cell(row, column, fire_cell)

@when(u'the fight starts')
def step_impl(context):
    row, column = 0, 0
    ice_cell = context.state.board.get_cells(row, column)[0]
    fire_cell = context.state.board.get_cells(row, column)[1]
    ice_cell.fight(fire_cell)

@then(u'the FireCell disappears from the battlefield')
def step_impl(context):
    assert len(context.state.board.get_cells(0, 0)) == 1
    assert isinstance(context.state.board.get_cells(0, 0)[0], IceCell)
    assert context.state.board.get_cells(0, 0)[0].get_level() == 1