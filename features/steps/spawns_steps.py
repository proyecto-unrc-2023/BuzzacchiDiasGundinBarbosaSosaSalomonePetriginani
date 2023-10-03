from logic.board import Board
from logic.spawn import Spawn, IceSpawn, FireSpawn
from logic.game_state import GameMode, GameState
###Scenario: First ice spawn
@given(u'that the setup phase has been completed')
def step_impl(context):
  pass

@given(u'the game is waiting for put the ice spawn')
def step_impl(context):
  context.state.new_game(rows = 50, columns = 50)
  assert context.state.mode == GameMode.SPAWN_PLACEMENT

@when(u'the user choose the position ({row:d}, {column:d}) for the ice spawn and the ice spawn will create in the position ({row:d}, {column:d})')
def step_impl(context, row, column):
  spawn = IceSpawn()
  context.state.add_spawn(rows = row, columns = column, spawn = spawn)

@then(u'the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION after the user put the ice spawn')
def step_impl(context):
  assert context.state.mode == GameMode.SIMULATION


###Scenario: First fire spawn

@given(u'the game is waiting for put the fire spawn')
def step_impl(context):
  context.state.new_game(rows = 50, columns = 50)
  assert context.state.mode == GameMode.SPAWN_PLACEMENT

@when(u'the user choose the position ({row:d}, {column:d}) for the fire spawn and the fire spawn will create in the position ({row:d}, {column:d})')
def step_impl(context, row, column):
  spawn = FireSpawn()
  context.state.add_spawn(rows = row, columns = column, spawn = spawn)

@then(u'the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION after the user put the fire spawn')
def step_impl(context):
  assert context.state.mode == GameMode.SIMULATION
