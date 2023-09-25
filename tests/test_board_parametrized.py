import pytest

from logic.board import Board

empty_board_params = [
    (4, 4, ' | | | \n'\
           ' | | | \n'\
           ' | | | \n'\
           ' | | | '),
    (2, 4, ' | | | \n'\
           ' | | | '),
    (2, 2, ' | \n' \
           ' | '),
    (6, 5, ' | | | | \n'\
           ' | | | | \n'\
           ' | | | | \n'\
           ' | | | | \n'\
           ' | | | | \n'\
           ' | | | | '),
    (50, 50, (' |'*49 + ' \n')*49 + ' |'*49 + ' ')
]

@pytest.mark.parametrize("rows, columns, expected", empty_board_params)
def test_empty_board_to_string(rows, columns, expected):
    board = Board(rows, columns)
    res = board.__str__()
    assert expected == res
