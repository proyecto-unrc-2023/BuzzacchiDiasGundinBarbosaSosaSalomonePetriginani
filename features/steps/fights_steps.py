from logic.cell import IceCell, FireCell, DeadCell, Cell, Level
from logic.board import Board
from behave import given, when, then


##########Scenario #1: Two level 1 cells fights
@given(u'there are two cells, one IceCell with 8 life points and one FireCell with 5 life points level 1 in position ({row:d},{column:d})')
def step_impl(context, row, column):
    context.state.board = Board(50, 50)  

    ice_cell = IceCell(level=Level.LEVEL_1, board=context.state.board, life=8, position=(row,column))
    fire_cell = FireCell(level=Level.LEVEL_1, board=context.state.board, life=5, position=(row,column))
    
    context.state.board.add_cell(row, column, ice_cell)
    context.state.board.add_cell(row, column, fire_cell)

@when(u'the fight starts')
def step_impl(context):
    row, column = 0, 0
    ice_cell = context.state.board.get_cells(row, column)[0]
    fire_cell = context.state.board.get_cells(row, column)[1]
    ice_cell.fight(fire_cell)

@then(u'the FireCell disappears from the battlefield and the IceCell wins with 4 life points')
def step_impl(context):
    assert len(context.state.board.get_cells(0, 0)) == 1
    assert isinstance(context.state.board.get_cells(0, 0)[0], IceCell)
    assert context.state.board.get_cells(0, 0)[0].get_life() == 4
    assert context.state.board.get_cells(0, 0)[0].get_level() == 1



##########Scenario #2: two level 3 cells fights
@given(u'there are two level 3 cells, one IceCell with 58 life points and one FireCell with 50 life points in position ({row:d},{column:d})')
def step_impl(context, row, column):
    context.state.board = Board(50, 50)  

    ice_cell = IceCell(level=Level.LEVEL_3, board=context.state.board, life=58, position=(row,column))
    fire_cell = FireCell(level=Level.LEVEL_3, board=context.state.board, life=50, position=(row,column))
    
    context.state.board.add_cell(row, column, ice_cell)
    context.state.board.add_cell(row, column, fire_cell)

@when(u'the fight begins')
def step_impl(context):
    row, column = 1, 1
    ice_cell = context.state.board.get_cells(row, column)[0]
    fire_cell = context.state.board.get_cells(row, column)[1]
    ice_cell.fight(fire_cell)

@then(u'the FireCell disappears and the IceCell wins with 54 life points')
def step_impl(context):
    assert len(context.state.board.get_cells(1, 1)) == 1
    assert isinstance(context.state.board.get_cells(1, 1)[0], IceCell)
    assert context.state.board.get_cells(1, 1)[0].get_life() == 54
    assert context.state.board.get_cells(1, 1)[0].get_level() == Level.LEVEL_3



##########Scenario #3: one level 1 IceCell against a level 2 FireCell
@given(u'there is one level 1 IceCell with 9 life points and one level 2 FireCell with 22 life points in position ({row:d},{column:d})')
def step_impl(context, row, column):
    context.state.board = Board(50, 50)  

    ice_cell = IceCell(level=Level.LEVEL_1, board=context.state.board, life=9, position=(row,column))
    fire_cell = FireCell(level=Level.LEVEL_2, board=context.state.board, life=22, position=(row,column))
    
    context.state.board.add_cell(row, column, ice_cell)
    context.state.board.add_cell(row, column, fire_cell)

@when(u'the fight commences')
def step_impl(context):
    row, column = 2, 2
    ice_cell = context.state.board.get_cells(row, column)[0]
    fire_cell = context.state.board.get_cells(row, column)[1]
    ice_cell.fight(fire_cell)

@then(u'the IceCell dies and the FireCell stays in the position with 18 life points and level 1')
def step_impl(context):
    assert len(context.state.board.get_cells(2, 2)) == 1
    assert isinstance(context.state.board.get_cells(2, 2)[0], FireCell)
    assert context.state.board.get_cells(2, 2)[0].get_life() == 18
    assert context.state.board.get_cells(2, 2)[0].get_level() == Level.LEVEL_1


##########Scenario #4: two fights, followed by an additional third one
@given(u'there are two level 2 cells in position ({row:d},{column:d}), one FireCell with 22 life points and one IceCell with 25 life points')
def step_impl(context, row, column):
    context.state.board = Board(50, 50)  
    fire_cell = FireCell(level=Level.LEVEL_2, board=context.state.board, life=22, position=(row,column))
    ice_cell = IceCell(level=Level.LEVEL_2, board=context.state.board, life=25, position=(row,column))
    context.state.board.add_cell(row, column, fire_cell)
    context.state.board.add_cell(row, column, ice_cell)

@given(u'there are two cells level 1 in position ({row:d},{column:d}), one IceCell with 12 life points and one FireCell with 15 life points')
def step_impl(context, row, column):
    ice_cell_level1 = IceCell(level=Level.LEVEL_1, board=context.state.board, life=12, position=(row,column))
    fire_cell_level1 = FireCell(level=Level.LEVEL_1, board=context.state.board, life=15, position=(row,column))
    context.state.board.add_cell(row, column, ice_cell_level1)
    context.state.board.add_cell(row, column, fire_cell_level1)

@when(u'the cells with same level start the fight')
def step_impl(context):
    row, column = 0, 0
    cells_in_position = context.state.board.get_cells(row, column)
    if len(cells_in_position) == 4:
        level2FireCell = cells_in_position[0]
        level2IceCell = cells_in_position[1]
        level1IceCell = cells_in_position[2]
        level1FireCell = cells_in_position[3]
        context.state.level1IceCell = level1IceCell
        context.state.level2FireCell = level2FireCell
        level2FireCell.fight(level2IceCell)
        level1IceCell.fight(level1FireCell)

@then(u'level 1 IceCell dies and FireCell level 1 wins now with 11 life points')
def step_impl(context):
    row, column = 0, 0
    cells_in_position = context.state.board.get_cells(row, column)
    assert len(cells_in_position) == 2
    assert context.state.level1IceCell not in cells_in_position
    assert cells_in_position[1].get_life() == 11
    assert cells_in_position[1].get_level() == Level.LEVEL_1
    assert isinstance(cells_in_position[1], FireCell)

@then(u'level 2 FireCell loses fight and level 2 IceCell wins with 21')
def step_impl(context):
    row, column = 0, 0
    cells_in_position = context.state.board.get_cells(row, column)
    assert len(cells_in_position) == 2
    assert isinstance(cells_in_position[0], IceCell)
    assert cells_in_position[0].get_life() == 21
    assert cells_in_position[0].get_level() == Level.LEVEL_2

@then(u'fight starts with the winning cells, FireCell with 11 life points against IceCell with 21')
def step_impl(context):
    row, column = 0, 0
    fire_cell = context.state.board.get_cells(row,column)[0]
    ice_cell = context.state.board.get_cells(row,column)[1]
    fire_cell.fight(ice_cell)

@then(u'IceCell finally wins with 17 health points and became level 1, and the FireCell dies')
def step_impl(context):
    assert len(context.state.board.get_cells(0 ,0)) == 1
    assert isinstance(context.state.board.get_cells(0 ,0)[0], IceCell)
    assert context.state.board.get_cells(0 ,0)[0].get_life() == 17
    assert context.state.board.get_cells(0 ,0)[0].get_level() == Level.LEVEL_1


##########Scenario #5: A higher-level cell fights against lower-level cells
@given(u'there is one FireCell with {life:d} life points at level 2 and two IceCells at level 1 with {ice_cell_life:d} life points each in position ({row:d},{column:d})')
def step_impl(context, life, ice_cell_life, row, column):
    context.state.board = Board(50, 50)
    fire_cell = FireCell(level=Level.LEVEL_2, board=context.state.board, life=life, position=(row, column))
    
    ice_cell1 = IceCell(level=Level.LEVEL_1, board=context.state.board, life=ice_cell_life, position=(row, column))
    ice_cell2 = IceCell(level=Level.LEVEL_1, board=context.state.board, life=ice_cell_life, position=(row, column))
    
    context.state.board.add_cell(row, column, fire_cell)
    context.state.board.add_cell(row, column, ice_cell1)
    context.state.board.add_cell(row, column, ice_cell2)

@when(u'the fight initiates')
def step_impl(context):
    row, column = 0, 0
    while True:
        cells_in_position = context.state.board.get_cells(row, column)
        if len(cells_in_position) <= 1:
            break
        fire_cell = cells_in_position[0]
        ice_cell = cells_in_position[1]
        fire_cell.fight(ice_cell)

@then(u'the FireCell at level {level:d} wins, the IceCells disappear from the battlefield, and the FireCell wins with {final_life:d} life points')
def step_impl(context, level, final_life):
    row, column = 0, 0
    cells_in_position = context.state.board.get_cells(row, column)
    assert len(cells_in_position) == 1
    remaining_cell = cells_in_position[0]
    assert isinstance(remaining_cell, FireCell)
    assert remaining_cell.get_level() == level
    assert remaining_cell.get_life() == final_life



