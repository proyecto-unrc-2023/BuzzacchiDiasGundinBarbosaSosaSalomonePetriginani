from logic.cell import IceCell, FireCell, Level
from logic.game_controller import GameController
from logic.game_state import GameMode, Team

from logic.spawn import IceSpawn
from logic.cell import Level
from behave import given, when, then

##########BACKGROUND
@given(u'a new game is started in Spawn Placement mode')
def step_impl(context):
    context.GameController.new_game(rows=50, columns=50)
    assert context.GameController.get_mode() == GameMode.SPAWN_PLACEMENT

@given(u'a user with username {username} is logged selecting team {team}')
def step_impl(context, username, team):
    context.GameController.set_username(username)
    context.GameController.set_team(Team(team))

@given(u'the user selects to put IceSpawn at the following positions')
def step_impl(context):
    positions = []
    for row_data in context.table:
        row = int(row_data["row"])
        column = int(row_data["column"])
        positions.append((row, column))
    context.GameController.add_spawn(positions)

    for position in positions:
        row, column = position
        spawn = context.GameController.get_board().get_cells(row, column)[0]
        assert isinstance(spawn, IceSpawn), f"Expected IceSpawn at position ({row}, {column}), but found {type(spawn).__name__}"

@given(u'simulation starts')
def step_impl(context):
    context.GameController.get_mode() == GameMode.SIMULATION

@given(u'a level {level:d} {cell_type} with {life_points:d} life points at position ({row:d},{column:d})')
def step_impl(context, level, cell_type, life_points, row, column):
    context.position = row,column
    if cell_type == 'FireCell':
        context.GameController.create_cell(row, column, Team.FireTeam, Level(level), life_points)
    else:
        context.GameController.create_cell(row, column, Team.IceTeam, Level(level), life_points)

@when(u'the fight starts')
def step_impl(context):
    context.fire_cell_before_fight = 0
    context.ice_cell_before_fight = 0
    for cell in context.GameController.get_cells(*context.position):
        if isinstance(cell,FireCell):
            context.fire_cell_before_fight += 1
        else:
            context.ice_cell_before_fight += 1
    context.GameController.execute_fights()

@then(u'the number of {cell_type} should be reduced by {cells_reduced:d}')
def step_impl(context, cell_type, cells_reduced):
    print(str(context.GameController.get_board()))

    if cell_type == 'FireCells':
        losing_cell_type = FireCell
        before_count = context.fire_cell_before_fight
    else:
        losing_cell_type = IceCell
        before_count = context.ice_cell_before_fight

    counter = 0
    for cell in context.GameController.get_cells(*context.position):
        if isinstance(cell, losing_cell_type):
            counter += 1

    assert counter == before_count - cells_reduced
    
@then(u'the {cell_type} should win with {life_points:d} life points and level {level:d}')
def step_impl(context, cell_type, life_points, level):
    if cell_type == 'FireCell':
        winning_cell_type = FireCell
    else: 
        winning_cell_type = IceCell
    cells = context.GameController.get_cells(*context.position)
    winning_cells = [cell for cell in cells if isinstance(cell, winning_cell_type)]
    matching_cells = [cell for cell in winning_cells if cell.life == life_points and cell.level == level]
    assert len(matching_cells) > 0











