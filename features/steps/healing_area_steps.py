from behave import given, when, then
from logic.board import Board
from logic.cell import IceCell, FireCell, DeadCell, Cell, Level
from logic.healing_area import HealingArea


#########
@given(u'there is a level 1 IceCell with 15 life points in position ({row:d},{column:d})')
def step_impl(context, row, column):
    context.state.board = Board(10, 10)
    ice_cell = IceCell(level=Level.LEVEL_1, board=context.state.board, life=15, position=(row,column))
    context.state.board.add_cell(row, column, ice_cell)

@given(u'a HealingArea affecting IceCells is at positions [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]')
def step_impl(context):
    healing_area_positions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
    context.state.ice_healing_area = HealingArea(board=context.state.board,
                                                 positions=healing_area_positions,
                                                 duration=20,
                                                 affected_cell_type=IceCell)

@when(u'the HealingArea effect is applied')
def step_impl(context):
    context.state.ice_healing_area.apply_effect()

@then(u'the IceCell at position ({row:d},{column:d}) should have {expected_life:d} life points')
def step_impl(context, row, column, expected_life):
    assert context.state.board.get_cells(row, column)[0].get_life() == expected_life


##########
@given(u'there is a level 1 IceCell with 19 life points in position ({row:d},{column:d})')
def step_impl(context, row, column):
    context.state.board = Board(10, 10)
    ice_cell = IceCell(level=Level.LEVEL_1, board=context.state.board, life=19, position=(row,column))
    context.state.board.add_cell(row, column, ice_cell)

@given(u'a HealingArea IceCells is at positions [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]')
def step_impl(context):
    healing_area_positions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
    context.state.ice_healing_area = HealingArea(board=context.state.board,
                                                 positions=healing_area_positions,
                                                 duration=20,
                                                 affected_cell_type=IceCell)

@when(u'healing area applies effect')
def step_impl(context):
    context.state.ice_healing_area.apply_effect()

@then(u'the IceCell at position ({row:d},{column:d}) should have {expected_life:d} life points')
def step_impl(context, row, column, expected_life):
    assert context.state.board.get_cells(row, column)[0].get_life() == expected_life

@then(u'the IceCell should level up to level 2')
def step_impl(context):
    assert context.state.board.get_cells(1, 1)[0].get_level() == Level.LEVEL_2


###
@given(u'there is a level 3 IceCell with 60 life points in position ({row:d},{column:d})')
def step_impl(context, row, column):
    context.state.board = Board(10, 10)
    ice_cell = IceCell(level=Level.LEVEL_3, board=context.state.board, life=60, position=(row,column))
    context.state.board.add_cell(row, column, ice_cell)

@given(u'an Ice healing area is at positions [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]')
def step_impl(context):
    healing_area_positions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
    context.state.ice_healing_area = HealingArea(board=context.state.board,
                                                 positions=healing_area_positions,
                                                 duration=20,
                                                 affected_cell_type=IceCell)

@when(u'the HealingArea heals')
def step_impl(context):
    context.state.ice_healing_area.apply_effect()

@then(u'the IceCell at position ({row:d},{column:d}) should remain at level 3 with 60 life points')
def step_impl(context, row, column):
    assert context.state.board.get_cells(row, column)[0].get_life() == 60
    assert context.state.board.get_cells(row, column)[0].get_level() == Level.LEVEL_3
