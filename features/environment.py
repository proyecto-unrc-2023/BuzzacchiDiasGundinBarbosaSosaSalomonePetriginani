from behave import fixture, use_fixture

from app import create_app
from logic.cell import DeadCell, FireCell, IceCell
from logic.game_controller import GameController


@fixture
def empire_client(context, *args, **kwargs):
    app = create_app("testing")
    app.testing = True
    context.client = app.test_client()
    ctx = app.test_request_context()
    ctx.push()
    yield context.client
    ctx.pop()

def before_feature(context, feature):
    # -- HINT: Recreate a new flaskr client before each feature is executed.
    use_fixture(empire_client, context)

def table_from_string(table):
    rows_list = []
    for row in table.rows:
        curr_row = []
        for elem in row:
            if elem == ' ':
                curr_row.append(str(DeadCell()))
            elif elem == 'F':
                curr_row.append(str(FireCell()))
            elif elem == 'I':
                curr_row.append(str(IceCell()))
            else:
                raise ValueError(f'Unknown cell value: {elem}')
        rows_list.append('|'.join(curr_row))
    return '\n'.join(rows_list)

@fixture
def game_controller(context):
    #, *args, **kwargs):
    context.GameController = GameController()
    # crear objeto
    yield context.GameController

def before_feature(context, feature):
    use_fixture(game_controller, context)
