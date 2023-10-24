from logic.board import Board
from logic.cell import Cell, IceCell, FireCell, DeadCell
from logic.spawn import Spawn, IceSpawn, FireSpawn
from logic.game_state import GameMode, GameState
from logic.game_controller import GameController
from behave import given, when, then


###Scenario: First ice spawn



@given(u'the user choose the position ({row:d}, {column:d}) for the {team} spawn')
def step_impl(context, row, column, team):
  pass

@when (u'the {team} spawn creates in the position ({row:d}, {column:d})')
def step_impl(context, row, column, team):
  context.GameController.create_spawn(row, column, team)

@then(u'the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION after the user put the Ice spawn')
def step_impl(context):
  assert context.GameController.get_mode() == GameMode.SIMULATION

###Scenario: First fire spawn

@given(u'the game is waiting for put the Fire spawn')
def step_impl(context):
  context.GameController.new_game(rows = 50, columns = 50)
  assert context.GameController.get_mode() == GameMode.SPAWN_PLACEMENT

#@when(u'the user choose the position ({row:d}, {column:d}) for the {team} spawn and the {team} spawn will create in the position ({row:d}, {column:d})')
#def step_impl(context, row, column, team):
#  context.GameController.create_spawn(row, column, team)

@then(u'the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION after the user put the Fire spawn')
def step_impl(context):
  assert context.GameController.get_mode() == GameMode.SIMULATION


###Scenario: Second ice spawn

@given(u'that the user is playing the game for team {team} and has spawn at position ({row:d}, {column:d})')
def step_impl(context, row, column, team):
  context.GameController.new_game(rows = 50, columns = 50)
  context.GameController.create_spawn(row, column, team)
  assert context.GameController.get_mode() == GameMode.SIMULATION

@given(u'the game is in the half game time and the game shows on the screen to choose the position of the second Ice spawn')
def step_impl(context):
  context.GameController.half_game()
  assert context.GameController.get_mode() == GameMode.SPAWN_PLACEMENT

@when(u'the user choose the position ({row:d}, {column:d}) for the {team} spawn and the second {team} spawn will create in the position ({row:d}, {column:d})')
def step_impl(context, row, column, team):
  context.GameController.create_spawn(row, column, team)

@then(u'the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION')
def step_impl(context):
  assert context.GameController.get_mode() == GameMode.SIMULATION


###Scenario: Second fire spawn

#@given(u'that the user is playing the game for team {team} and has spawn at position ({row:d}, {column:d})')
#def step_impl(context, row, column, team):
#  context.GameController.new_game(rows = 50, columns = 50)
#  context.GameController.create_spawn(row, column, team)
#  assert context.GameController.get_mode == GameMode.SIMULATION

@given(u'the {team} spawn creates in the position ({row:d},{column:d})')
def step_impl(context, row, column, team):
  context.GameController.create_spawn(row, column, team)


#@when(u'the user choose the position ({row:d}, {column:d}) for the {team} spawn and the second {team} spawn will create in the position ({row:d}, {column:d})')
#def step_impl(context, row, column, team):
#  context.GameController.create_spawn(row, column, team)
