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


###Scenario: Second ice spawn

@given(u'that the user is playing the game for team ice')
def step_impl(context):
  context.state.new_game(rows = 50, columns = 50)
  ice_spawn = IceSpawn()
  context.state.add_spawn(rows = 3, columns = 4, spawn = ice_spawn)
  assert context.state.mode == GameMode.SIMULATION

@given(u'the game is in the half game time and the game shows on the screen to choose the position of the second ice spawn')
def step_impl(context):
  context.state.half_game()
  assert context.state.mode == GameMode.SPAWN_PLACEMENT

@when(u'the user choose the position ({row:d}, {column:d}) for the ice spawn and the second ice spawn will create in the position ({row:d}, {column:d})')
def step_impl(context, row, column):
  ice_spawn2 = IceSpawn()
  context.state.add_spawn(row, column, ice_spawn2)

@then(u'the gamemode changes from GameMode.SPAWN_PLACEMENT to GameMode.SIMULATION')
def step_impl(context):
  assert context.state.mode == GameMode.SIMULATION


###Scenario: Second fire spawn
@given(u'that the user is playing the game for team fire')
def step_impl(context):
  context.state.new_game(rows = 50, columns = 50)
  fire_spawn = FireSpawn()
  context.state.add_spawn(rows = 3, columns = 4, spawn = fire_spawn)
  assert context.state.mode == GameMode.SIMULATION

@given(u'the game is in the half game time and the game shows on the screen to choose the position of the second fire spawn')
def step_impl(context):
  context.state.half_game()
  assert context.state.mode == GameMode.SPAWN_PLACEMENT

@when(u'the user choose the position ({row:d}, {column:d}) for the fire spawn and the second fire spawn will create in the position ({row:d}, {column:d})')
def step_impl(context, row, column):
  fire_spawn2 = FireSpawn()
  context.state.add_spawn(row, column, fire_spawn2)
