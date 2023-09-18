
from features.environment import table_from_string
from logic.game_state import GameState, GameMode


@given(u'the game is not started')
def step_impl(context):
    pass


@when(u'we create a new game with an {rows:d}x{columns:d} board')
def step_impl(context, rows, columns):
    context.state.new_game(rows, columns)

@then(u'the game should be in spawn placement mode')
def step_impl(context):
    assert context.state.mode == GameMode.SPAWN_PLACEMENT

@then(u'the state of the board should be a 50x50 empty board')
def step_impl(context):
    emptyboard_50x50 = (' |'*49 + ' \n')*49 + ' |'*49 + ' '
    assert context.state.board.__str__() == emptyboard_50x50
