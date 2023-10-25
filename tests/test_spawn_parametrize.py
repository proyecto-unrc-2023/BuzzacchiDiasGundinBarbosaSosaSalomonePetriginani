import pytest

from logic.spawn import IceSpawn, FireSpawn
from logic.board import Board
from logic.cell import IceCell, FireCell, Level

@pytest.fixture
def board():
    return Board(50, 50)



######Only tests where Spawns wins are tested in this methods cause if Spawn dies GameState method handles that case
@pytest.mark.parametrize("spawn_type, initial_life, cell_life, expected_result", [
    (IceSpawn, 300, 10, 290),     # IceSpawn vs. FireCell (IceSpawn wins)
    (IceSpawn, 300, 58, 242),     # IceSpawn vs. FireCell (FireCell wins)
    (FireSpawn, 300, 38, 262),   # FireSpawn vs. IceCell (FireSpawn wins)
])

def test_spawn_fight(board, spawn_type, initial_life, cell_life, expected_result):
    positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    spawn = spawn_type(life=initial_life, positions=positions, board=board)
    if cell_life <= 20:
        cell = IceCell(level=Level.LEVEL_1, life=cell_life, position=(0, 0), board=board)
    elif cell_life <= 40:
        cell = IceCell(level=Level.LEVEL_2, life=cell_life, position=(0, 0), board=board)
    else:
        cell = IceCell(level=Level.LEVEL_3, life=cell_life, position=(0, 0), board=board)

    board.add_spawn(positions, spawn)
    board.add_cell(0, 0, cell)

    spawn.fight(cell)

    assert spawn.get_life() == expected_result
    if spawn.get_life() == 0:
        for position in positions:
            assert spawn not in board.get_cells(*position)

    if expected_result > 0:
        assert cell not in board.get_cells(0, 0)
    else:
        assert cell in board.get_cells(0, 0)