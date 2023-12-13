from behave import given, when, then
from logic.board import Board
from logic.cell import IceCell, FireCell, DeadCell, Cell, Level
from logic.healing_area import HealingArea
from logic.game_state import GameMode, GameState
from logic.game_controller import GameController

# #########
# @given(u'there is a level {level:d} {cell_type} with {life:d} life points in position ({row:d},{column:d})')
# def step_impl(context, row, column, level, cell_type, life):
#     context.GameController.create_cell(row, column, cell_type, level, life)

# @given(u'a HealingArea affecting {team} is at position ({row:d},{column:d}) and its adjacent')
# def step_impl(context, row, column, team):
#     # context.GameController.create_healing_area(row, column, team)

# @when(u'the IceCell HealingArea effect is applied')
# def step_impl(context):
#     pass
#     #context.state.ice_healing_area.apply_effect()

# @then(u'the IceCell at position ({row:d},{column:d}) should have {expected_life:d} life points')
# def step_impl(context, row, column, expected_life):
#     assert context.GameController.get_cells(row, column)[0].get_life() == expected_life

@given(u'there is a level {level:d} {cell_type} with {life:d} life points in position ({row:d},{column:d})')
def step_impl(context, level, cell_type, life, row, column):
    context.GameController.create_cell(row, column, cell_type, level, life)

@given(u'a HealingArea affecting {cell_type} is at position ({row:d},{column:d}) and its adjacent')
def step_impl(context, row, column, cell_type):
    context.GameController.create_healing_area(row, column, cell_type)

@when(u'the IceCell HealingArea effect is applied')
def step_impl(context):
    context.GameController.apply_healing()

@when(u'the FireCell HealingArea effect is applied')
def step_impl(context):
    context.GameController.apply_healing()

@then(u'the IceCell at position ({row:d},{column:d}) is upgraded to level {level:d}')
def step_impl(context, level, row, column):
    assert context.GameController.get_cells(row, column)[0].get_level() == Level(level)

@then(u'the FireCell at position ({row:d},{column:d}) should remain at level {level:d} with {life:d} life points')
def step_impl(context, level, row, column, life):
    assert context.GameController.get_cells(row, column)[0].get_level() == Level(level)
    assert context.GameController.get_cells(row, column)[0].get_life() == life
    #current_level = context.GameController.get_cells(row, column)[0].get_level()
    #current_life = context.GameController.get_cells(row, column)[0].get_life()
    #print(f"Current Level: {current_level}, Current Life: {current_life}")
    #assert current_level == Level(level) and current_life == life



##########
#@given(u'there is a level 1 IceCell with 19 life points in position ({row:d},{column:d})')
#def step_impl(context, row, column):
#    context.state.board = Board(10, 10)
#    ice_cell = IceCell(level=Level.LEVEL_1, board=context.state.board, life=19, position=(row,column))
#    context.state.board.add_cell(row, column, ice_cell)

#@given(u'a HealingArea affecting IceCells is at positions [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]')
#def step_impl(context):
#    healing_area_positions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
#    context.state.ice_healing_area = HealingArea(board=context.state.board,
#                                                 positions=healing_area_positions,
#                                                 duration=20,
#                                                 affected_cell_type=IceCell)

#@when(u'healing area applies effect')
#def step_impl(context):
#    context.state.ice_healing_area.apply_effect()

#there is a level 1 IceCell with 15 life points in the same position with the healing area
@given(u'there is a level {level:d} {team} with {life:d} life points in the same position with the healing area')
def step_impl(context, level, team, life):
    pos_healing = context.GameController.get_positions_healing(team)
    pos = pos_healing[3]
    context.GameController.create_cell(pos[0], pos[1], team, level, life)
    
#@when(u'the IceCell HealingArea effect is applied')
#def step_impl(context):
#    context.GameController.apply_healing()

@then(u'the {team} should have {life:d} life points')
def step_impl(context, team, life):
    pos_healing = context.GameController.get_positions_healing(team)
    pos = pos_healing[3]
    assert context.GameController.get_cells(pos[0], pos[1])[0].get_life() == life


#@then(u'the IceCell should level up to level 2')
#def step_impl(context):
#    assert context.state.board.get_cells(1, 1)[0].get_level() == Level.LEVEL_2


###
#@given(u'there is a level 3 IceCell with 60 life points in position ({row:d}, {column:d})')
#def step_impl(context, row, column):
#    context.state.board = Board(10, 10)
#    ice_cell = IceCell(level=Level.LEVEL_3, board=context.state.board, life=60, position=(row,column))
#    context.state.board.add_cell(row, column, ice_cell)

#@given(u'an Ice healing area is at positions [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]')
#def step_impl(context):
#    healing_area_positions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
#    context.state.ice_healing_area = HealingArea(board=context.state.board,
#                                                 positions=healing_area_positions,
#                                                 duration=20,
#                                                 affected_cell_type=IceCell)

#@when(u'the HealingArea heals')
#def step_impl(context):
#    context.state.ice_healing_area.apply_effect()

# @then(u'the IceCell at position ({row:d},{column:d}) should remain at level {level:d} with {life:d} life points')
# def step_impl(context, row, column, level, life):
#     assert context.GameController.get_cells(row, column)[0].get_life() == life
#     assert context.GameController.get_cells(row, column)[0].get_level() == level
