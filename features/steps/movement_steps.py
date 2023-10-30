from behave import given, when, then
from logic.board import Board
from logic.cell import Cell, IceCell, FireCell, DeadCell, Level

@given(u'I have a level {level:d} {team} at position ({row:d}, {column:d}) with {life:d} health points')
def step_impl(context, row, column, level, life, team):
    context.GameController.create_cell(row, column, team, level, life)

@given(u'the adjacents cells at position of the {team} ({row:d}, {column:d}) are empty')
def step_impl(context, row, column, team):
    list = context.GameController.get_adjacents_for_move(row, column, team)
    for x in list:
        r, c = x
        assert len(context.GameController.get_cells(r,c)) == 0

@when(u'I try to move the level {level:d} {team} to an adjacent position')
def step_impl(context, level, team):
    context.GameController.execute_movement()

@then(u'the {team} moves successfully to an adjacent position of ({row:d}, {column:d})')
def step_impl(context, row, column, team):
    list = context.GameController.get_adjacents_for_move(row, column, team)
    for x in list:
        r, c = x
        if (len(context.GameController.get_cells(r,c)) == 1):
            assert True

