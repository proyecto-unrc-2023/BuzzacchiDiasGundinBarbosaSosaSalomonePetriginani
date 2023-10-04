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

@when(u'first battle starts, level 2 cells fight ends with IceCell winning with 21 life points and second battle starts, winning cell fights with level 1 FireCell, that finishes with a win for the same cell again')
def step_impl(context):
    row, column = 0, 0
    context.state.board.execute_fight_in_position(row,column)

@then(u'we have two IceCells, level 1 cell with no fights, and the cells with 2 fights became level 1 with 17 life points')
def step_impl(context):
    row, column = 0, 0
    cells_in_position = context.state.board.get_cells(row, column)
    assert len(cells_in_position) == 2
    assert cells_in_position[0].get_life() == 17
    assert cells_in_position[1].get_level() == Level.LEVEL_1
    assert cells_in_position[0].get_level() == Level.LEVEL_1
    assert all(isinstance(cell, IceCell) for cell in cells_in_position)



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
    context.state.board.execute_fight_in_position(row,column)

@then(u'the FireCell at level {level:d} wins, the IceCells disappear from the battlefield, and the FireCell wins with {final_life:d} life points')
def step_impl(context, level, final_life):
    row, column = 0, 0
    cells_in_position = context.state.board.get_cells(row, column)
    assert len(cells_in_position) == 1
    remaining_cell = cells_in_position[0]
    assert isinstance(remaining_cell, FireCell)
    assert remaining_cell.get_level() == level
    assert remaining_cell.get_life() == final_life



