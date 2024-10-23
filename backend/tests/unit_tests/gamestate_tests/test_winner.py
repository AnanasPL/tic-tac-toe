import pytest

from errors import *

from ...fixtures import gs


class TestWinner:
    def test_get_winner_when_there_is_no_yet(self, gs):
        assert gs.get_winner() is None
        
    def test_get_winner_first_player_won(self, gs):
        gs.update_board_state(0, 'XXX')
        gs.update_board_state(1, 'YYY')
        gs.update_board_state(4, 'XXX')
        gs.update_board_state(2, 'YYY')
        gs.update_board_state(8, 'XXX')
        
        assert gs.get_winner() is gs.get_player_by_session_id('XXX')
    
    def test_get_winner_second_player_won(self, gs):
        gs.update_board_state(1, 'XXX')
        gs.update_board_state(0, 'YYY')
        gs.update_board_state(2, 'XXX')
        gs.update_board_state(4, 'YYY')
        gs.update_board_state(3, 'XXX')
        gs.update_board_state(8, 'YYY')
        
        assert gs.get_winner() is gs.get_player_by_session_id('YYY')
        
    def test_get_winner_tie(self, gs):
        gs.update_board_state(0, 'XXX')
        gs.update_board_state(8, 'YYY')
        gs.update_board_state(1, 'XXX')
        gs.update_board_state(7, 'YYY')
        gs.update_board_state(6, 'XXX')
        gs.update_board_state(2, 'YYY')
        gs.update_board_state(5, 'XXX')
        gs.update_board_state(3, 'YYY')
        gs.update_board_state(4, 'XXX')
        
        assert gs.get_winner() == 'tie'
        