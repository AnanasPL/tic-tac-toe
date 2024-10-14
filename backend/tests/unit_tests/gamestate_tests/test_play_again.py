import pytest

from errors import *

from .fixtures import gs

class TestPlayAgain:
    def test_wants_to_play_again(self, gs):
        gs.player_wants_to_play_again('XXX', True)
        gs.player_wants_to_play_again('YYY', False)
        
        assert gs.get_player_info('XXX')['wantsToPlayAgain']
        assert not gs.get_player_info('YYY')['wantsToPlayAgain']
    
    def test_player_wants_to_play_again_invalid_player_session_id(self, gs):
        with pytest.raises(PlayerNotFoundError):
            gs.player_wants_to_play_again('ZZZ', False)
            
    @pytest.mark.parametrize('decision1, decision2, expected_output', [
        (True, True, True),
        (True, False, False),
        (False, True, False),
        (False, False, False)
    ])
    def test_all_players_want_to_play_again(self, gs, decision1, decision2, expected_output):
        gs.player_wants_to_play_again('XXX', decision1)
        gs.player_wants_to_play_again('YYY', decision2)
        
        assert gs.all_players_want_to_play_again() == expected_output
        
           