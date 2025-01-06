import pytest

from game.board import Board
from errors import *

class TestWinCombinations:
    @pytest.mark.parametrize('id1, id2, id3', [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
        ])
    def test_winning_combinations(self, id1, id2, id3):
        b = Board()
        b.update(id1, 'X')
        b.update(id2, 'X')
        b.update(id3, 'X')

        assert b.get_winner() == 'X'
        
    def test_tie(self):
        b = Board()
        
        b.update(0, 'X')
        b.update(8, 'O')
        b.update(1, 'X')
        b.update(7, 'O')
        b.update(6, 'X')
        b.update(2, 'O')
        b.update(4, 'X')
        b.update(3, 'O')
        b.update(5, 'X')
        
        assert b.get_winner() == 'tie'
        
    def test_update_after_game_end(self):
        b = Board()
        b.update(0, 'X')
        b.update(1, 'X')
        b.update(2, 'X')
        b.get_winner()
        
        with pytest.raises(GameAlreadyFinishedError):
            b.update(4, 'X')