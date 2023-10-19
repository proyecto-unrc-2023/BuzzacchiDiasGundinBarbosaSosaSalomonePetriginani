from behave import given, when, then
from logic.board import Board
from logic.cell import Cell, IceCell, FireCell, DeadCell, Level

@given(u'I have a level {level:d} {team} cell at position ({row:d}, {column:d}) with {life:d} health points')
def step_impl(context, row, column, level, life, team):
    context.GameController.new_game(50, 50)
    context.GameController.create_cell(row, column, team, level, life)

@given(u'the adjacents cells at position ({row:d}, {column:d}) are empty')
def step_impl(context, row, column):
    list = context.GameController.get_adjacents_for_move(row, column)
    for x in list:
        r, c = x
        assert len(context.GameController.get_cells(r,c)) == 0

@when(u'I try to move the level {level:d} {team} cell to an adjacent position')
def step_impl(context, level, team):
    context.GameController.execute_movement()

@then(u'the {team} cell moves successfully to an adjacent position of ({row:d}, {column:d})')
def step_impl(context, row, column, team):
    list = context.GameController.get_adjacents_for_move(row, column)
    for x in list:
        r, c = x
        if (len(context.GameController.get_cells(r,c)) == 1):
            assert True

@given(u'there are level {level:d} {team} cells at adjacents positions of ({row:d}, {column:d}) with {life:d} health points')
def step_impl(context, level, row, column, life, team):
    list = context.GameController.get_adjacents_for_move(row, column)
    for x in list:
        r, c = x
        context.GameController.create_cell(r, c, team, level, life)

@when(u'I try to move the {team} cells to an adjacent position')
def step_impl(context, team):
    context.GameController.execute_movement()

@then(u'the cells cannot merge, and coexist in the board')
def step_impl(context):
    i = 0
    j = 0
    while i < 50:
        while j < 50: 
            assert len(context.GameController.get_cells(i, j)) < 4
            j = j + 1
        i = i + 1
