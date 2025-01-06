import pytest

from game.gamestate import GameState
from errors import *

class TestRemovePlayer:
    def test_remove_player(self):
        gs = GameState()
        gs.add_player('XXX')
        gs.remove_player('XXX')
        
        assert 'XXX' not in gs.get_players_session_ids()
        
    def test_remove_player_that_is_not_in_the_room(self):
        gs = GameState()
        gs.add_player('XXX')
        
        with pytest.raises(PlayerNotFoundError):
            gs.remove_player('ZZZ')
