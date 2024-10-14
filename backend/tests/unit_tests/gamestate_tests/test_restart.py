import pytest

from errors import *
from .fixtures import gs

# Some changes to the initial state
@pytest.fixture
def gs2(gs):
    gs.update_board_state(0, 'XXX')
    gs.update_board_state(8, 'YYY')
    gs.update_board_state(1, 'XXX')
    
    gs.player_wants_to_play_again('XXX', True)
    gs.player_wants_to_play_again('YYY', False)
    
    return gs


class TestRestartGame:
    def test_board_clear(self, gs2):
        gs2.restart_game()
        
        assert gs2.get_board_state() == ['' for _ in range(9)]
        
    def test_reverse_symbols(self, gs2):
        gs2.restart_game()
        
        assert gs2.get_player_info('XXX')['symbol'] == 'X'
        assert gs2.get_player_info('YYY')['symbol'] == 'O'
        
    def test_determine_turns_again(self, gs2):
        gs2.restart_game()
        
        assert not gs2.get_player_info('XXX')['isCurrentPlayer']
        assert gs2.get_player_info('YYY')['isCurrentPlayer']
        
    def test_reset_wants_to_play_again(self, gs2):
        gs2.restart_game()
        
        assert gs2.get_player_info('XXX')['wantsToPlayAgain'] is None
        assert gs2.get_player_info('YYY')['wantsToPlayAgain'] is None