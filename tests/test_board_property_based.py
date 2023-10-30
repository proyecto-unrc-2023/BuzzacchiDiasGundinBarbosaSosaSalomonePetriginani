import pytest

from logic.board import Board


property_based_test_params = [
    (' | | | \n'
     ' | | | \n'
     ' | | | \n'
     ' | | | '),
     (' | | | \n'\
      ' | | | '),
     (' | \n' \
      ' | '),
     (' |I\n' \
      'I| '),
     ('F,I| \n'\
      ' | '),
     ('F|I|F\n'
      'I|F|I\n'
      'F|I|F'),
    ('F,I|F,I|F,I\n'\
     'F,I|F,I|F,I'),
     ('IS|IS|IS| | | | | \n'\
      'IS|IS|IS| | | | | \n'
      'IS|IS|IS| | | | | \n'
      ' | | | | | | | \n'
      ' | | | | | | | \n'
      ' | | | | |FS,I|FS|FS\n'
      ' | | | | |FS|FS|FS\n'
      ' | | | | |FS|FS|FS')
]

@pytest.mark.parametrize("board_str", property_based_test_params)
def test_board_from_string(board_str):
    board = Board.from_string(board_str)
    assert board.__str__() == board_str
