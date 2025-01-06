import pytest

from game.board import Board
from errors import *

class TestUpdateBoard:
    @pytest.mark.parametrize('index', [-1, 9])
    def test_update_board_invalid_index(self, index):
        b = Board()
        
        with pytest.raises(IndexError):
            b.update(index, 'X')
            
    def test_update_board_invalid_field(self):
        b = Board()
        b.update(0, 'X')
        
        with pytest.raises(FieldAlreadyTakenError):
            b.update(0, 'O')
            
    @pytest.mark.parametrize('index', [i for i in range(9)])
    def test_update_board_state(self, index):
        b = Board()
        b.update(index, 'X')
        
        assert b.get_state()[index] == 'X'
        
    def test_clear_board(self):
        b = Board()
        b.update(0, 'X')
        b.update(1, 'O')
        b.update(2, 'X')
        b.update(3, 'O')
        b.update(4, 'X')
        
        b.clear()
        
        assert b.get_state() == ['' for _ in range(9)]
        
    