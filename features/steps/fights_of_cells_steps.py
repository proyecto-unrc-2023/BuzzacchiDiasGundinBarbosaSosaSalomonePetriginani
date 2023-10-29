
from logic.spawn import IceSpawn
from logic.cell import Level, IceCell, FireCell
from logic.game_state import GameMode, GameState, Team
from behave import given, when, then
#from typing import Type

##########BACKGROUND
@given(u'a new game is started in Spawn Placement mode')
def step_impl(context):
    context.GameController.new_game(rows=50, columns=50)
    assert context.GameController.get_mode() == GameMode.SPAWN_PLACEMENT

@given(u'a user with username {username} is logged selecting team {team}')
def step_impl(context, username, team):
    context.GameController.set_username(username)
    context.GameController.set_team(Team(team))

@given(u'the user selects to put {spawn_type} at the position ({row:d},{column:d})')
def step_impl(context, row, column, spawn_type):
    context.GameController.create_spawn(row, column, spawn_type)
    positions_spawn = [(i,j) for i in range(row-1, row+2) for j in range(column-1, column+2)]
    print(str(context.GameController.get_board()))
    for pos in positions_spawn:
        assert isinstance(context.GameController.get_spawn(spawn_type), IceSpawn)

@given(u'simulation starts')
def step_impl(context):
    context.GameController.get_mode() == GameMode.SIMULATION



##########STEPS
@given(u'a level {level:d} {cell_type} with {life_points:d} life points at position ({row:d},{column:d})')
def step_impl(context, level, cell_type, life_points, row, column):
    context.position = row,column
    context.GameController.create_cell(row, column, cell_type, Level(level), life_points)

@when(u'the fight starts')
def step_impl(context):
    context.ice_cell_before_fight = len(context.GameController.get_ice_cells(*context.position))
    context.fire_cell_before_fight = len(context.GameController.get_fire_cells(*context.position))
    context.GameController.execute_fights()

@then(u'the number of {cell_type} should be reduced by {cells_reduced:d}')
def step_impl(context, cell_type, cells_reduced):
    row, column = context.position
    count_ice, count_fire = len(context.GameController.get_ice_cells(row, column)), len(context.GameController.get_fire_cells(row, column))
    if cell_type == 'FireCells':
        assert context.fire_cell_before_fight - count_fire == cells_reduced
    else:
        assert context.ice_cell_before_fight - count_ice == cells_reduced

@then(u'the {cell_type} should win with {life_points:d} life points and level {level:d}')
def step_impl(context, cell_type, life_points, level):
    matching_cells = context.GameController.find_matching_cells(context.position, cell_type, life_points, level)
    assert len(matching_cells) > 0
