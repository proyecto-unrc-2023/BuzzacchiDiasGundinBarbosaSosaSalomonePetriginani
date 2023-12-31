from logic.spawn import IceSpawn
from logic.cell import Level
from logic.game_state import GameMode, Team
from behave import given, when, then



##########STEPS
@given(u'the IceSpawn has {life_points:d} life points')
def step_impl(context, life_points):
    context.GameController.get_ice_spawn().set_life(life_points)

@then(u'the IceSpawn has {life_points:d} life points and the cell(s) dies')
def step_impl(context, life_points):
    print(context.GameController.get_ice_spawn().get_life())
    assert context.GameController.get_ice_spawn().get_life() == life_points
    assert len(context.GameController.get_cells_in_spawn(context.GameController.get_ice_spawn())) == 0

@then(u'the IceSpawn dies and the game ends')
def step_impl(context):
    assert context.GameController.get_mode() == GameMode.FINISHED
    assert context.GameController.get_ice_spawn().get_life() == 0