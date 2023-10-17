from logic.cell import IceCell, FireCell, Level
from logic.game_controller import GameController
from logic.game_state import GameMode, Team

from logic.spawn import IceSpawn
from logic.cell import Level
from behave import given, when, then


# @given(u'a new game is started in Spawn Placement mode')
# def step_impl(context):
#     context.state = GameController()
#     context.state.game_controller = GameController()
#     context.state.game_controller.new_game(rows=50, columns=50)
#     context.state.board = context.state.game_controller.get_board()  
#     assert context.state.game_controller.get_mode() == GameMode.SPAWN_PLACEMENT


##########BACKGROUND
####Given 2
@given(u'a new game is started in Spawn Placement mode')
def step_impl(context):
    context.state = {}  
    context.state['game_controller'] = GameController()  
    context.state['game_controller'].new_game(rows=50, columns=50)
    context.state['board'] = context.state['game_controller'].get_board()  
    assert context.state['game_controller'].get_mode() == GameMode.SPAWN_PLACEMENT


@given(u'a user with username {username} is logged selecting team {team}')
def step_impl(context, username, team):
    context.state['game_controller'].set_username(username)
    context.state['game_controller'].set_team(Team(team))


@given(u'the user selects to put IceSpawn at the following positions')
def step_impl(context):
    positions = []
    for row_data in context.table:
        row = int(row_data["row"])
        column = int(row_data["column"])
        positions.append((row, column))
    context.state['game_controller'].add_spawn(positions)
    #print(str(context.state['game_controller'].get_board()))

    for position in positions:
        row, column = position
        spawn = context.state['game_controller'].get_board().get_cells(row, column)[0]
        assert isinstance(spawn, IceSpawn), f"Expected IceSpawn at position ({row}, {column}), but found {type(spawn).__name__}"


@given(u'simulation starts')
def step_impl(context):
    context.state['game_controller'].get_mode() == GameMode.SIMULATION


@given(u'a level {level:d} {cell_type} with {life_points:d} life points at position ({row:d},{column:d})')
def step_impl(context, level, cell_type, life_points, row, column):
    context.state['position'] = row,column
    if cell_type == 'FireCell':
        context.state['game_controller'].create_cell(row, column, Team.FireTeam, Level(level), life_points)
    else:
        context.state['game_controller'].create_cell(row, column, Team.IceTeam, Level(level), life_points)

@when(u'the fight starts')
def step_impl(context):
    #print(str(context.state['game_controller'].get_board()))
    context.state['fire_cell_before_fight'] = 0
    context.state['ice_cell_before_fight'] = 0
    for cell in context.state['game_controller'].get_cells(*context.state['position']):
        if isinstance(cell,FireCell):
            context.state['fire_cell_before_fight'] += 1
        else:
            context.state['ice_cell_before_fight'] += 1
    context.state['game_controller'].execute_fights()

    print(str(context.state['game_controller'].get_cells(1,1)))

@then(u'the number of {cell_type} should be reduced by {cells_reduced:d}')
def step_impl(context, cell_type, cells_reduced):
    print(str(context.state['game_controller'].get_board()))

    if cell_type == 'FireCells':
        losing_cell_type = FireCell
        before_count = context.state['fire_cell_before_fight']
    else:
        losing_cell_type = IceCell
        before_count = context.state['ice_cell_before_fight']

    counter = 0
    for cell in context.state['game_controller'].get_cells(*context.state['position']):
        if isinstance(cell, losing_cell_type):
            counter += 1

    assert counter == before_count - cells_reduced
    
@then(u'the {cell_type} should win with {life_points:d} life points and level {level:d}')
def step_impl(context, cell_type, life_points, level):
    if cell_type == 'FireCell':
        winning_cell_type = FireCell
    else: 
        winning_cell_type = IceCell
    cells = context.state['game_controller'].get_cells(*context.state['position'])
    winning_cells = [cell for cell in cells if isinstance(cell, winning_cell_type)]
    matching_cells = [cell for cell in winning_cells if cell.life == life_points and cell.level == level]
    assert len(matching_cells) > 0







##########Scenario 1 y 2
@given(u'there are two level {level:d} cells, one IceCell with {ice_points:d} life points and one FireCell with {fire_points:d} life points in position ({row:d},{column:d})')
def step_impl(context, level, ice_points, fire_points, row, column):
    context.state.position = (row,column)

    ice_cell = IceCell(level=Level(level), board=context.state.board, life=ice_points, position=(row,column))
    fire_cell = FireCell(level=Level(level), board=context.state.board, life=fire_points, position=(row,column))
    
    context.state.board.add_cell(row, column, ice_cell)
    context.state.board.add_cell(row, column, fire_cell)



@then(u'the {loser_cell} disappears from the battlefield and the {winner_cell} wins with {winning_life_points:d} life points and level {winner_level:d}')
def step_impl(context, loser_cell, winner_cell, winning_life_points, winner_level):
    assert len(context.state.board.get_cells(*context.state.position)) == 1
    assert isinstance(context.state.board.get_cells(*context.state.position)[0], globals()[winner_cell])
    assert context.state.board.get_cells(*context.state.position)[0].get_life() == winning_life_points
    assert context.state.board.get_cells(*context.state.position)[0].get_level() == winner_level


##########Scenario #3: one level 1 IceCell against a level 2 FireCell
@given(u'there is one level 1 IceCell with 9 life points and one level 2 FireCell with 22 life points in position ({row:d},{column:d})')
def step_impl(context, row, column):
    context.state.position = (row,column)

    ice_cell = IceCell(level=Level.LEVEL_1, board=context.state.board, life=9, position=(row,column))
    fire_cell = FireCell(level=Level.LEVEL_2, board=context.state.board, life=22, position=(row,column))
    
    context.state.board.add_cell(row, column, ice_cell)
    context.state.board.add_cell(row, column, fire_cell)



##########Scenario #4: two fights, followed by an additional third one
@then(u'we have two IceCells, level 1 cell with no fights, and the cells with 2 fights became level 1 with 17 life points')
def step_impl(context):
    cells_in_position = context.state.board.get_cells(*context.state.position)
    assert len(cells_in_position) == 2
    assert cells_in_position[0].get_life() == 17
    assert cells_in_position[1].get_level() == Level.LEVEL_1
    assert cells_in_position[0].get_level() == Level.LEVEL_1
    assert all(isinstance(cell, IceCell) for cell in cells_in_position)



##########Scenario #5: A higher-level cell fights against lower-level cells
@given(u'there is one FireCell with {life:d} life points at level 2 and two IceCells at level 1 with {ice_cell_life:d} life points each in position ({row:d},{column:d})')
def step_impl(context, life, ice_cell_life, row, column):
    context.state.position = (row, column)
    fire_cell = FireCell(level=Level.LEVEL_2, board=context.state.board, life=life, position=(row, column))
    
    ice_cell1 = IceCell(level=Level.LEVEL_1, board=context.state.board, life=ice_cell_life, position=(row, column))
    ice_cell2 = IceCell(level=Level.LEVEL_1, board=context.state.board, life=ice_cell_life, position=(row, column))
    
    context.state.board.add_cell(row, column, fire_cell)
    context.state.board.add_cell(row, column, ice_cell1)
    context.state.board.add_cell(row, column, ice_cell2)

@then(u'the FireCell at level {level:d} wins, the IceCells disappear from the battlefield, and the FireCell wins with {final_life:d} life points')
def step_impl(context, level, final_life):
    cells_in_position = context.state.board.get_cells(*context.state.position)
    remaining_cell = cells_in_position[0]
    assert isinstance(remaining_cell, FireCell)
    assert len(cells_in_position) == 1
    assert remaining_cell.get_level() == level
    assert remaining_cell.get_life() == final_life



