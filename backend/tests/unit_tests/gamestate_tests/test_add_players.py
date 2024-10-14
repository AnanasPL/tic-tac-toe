import pytest

from rooms import Player, GameState
from errors import *

class TestAddPlayerToTheGameState:
    def test_add_player_to_the_game(self):
        gs = GameState()
        gs.add_player('XXX')
        
        assert 'XXX' in gs.get_players_session_ids()
        
    def test_add_player_that_is_already_in_the_room(self):
        gs = GameState()
        gs.add_player('XXX')
        gs.add_player('XXX')
        
        assert len(gs.players) == 1
        
    def test_add_player_to_a_full_game(self):
        gs = GameState()
        gs.add_player('XXX')
        gs.add_player('YYY')
        
        with pytest.raises(RoomAlreadyFullError):
            gs.add_player('ZZZ')
            
    def test_added_player_has_correct_symbol(self):
        gs = GameState()
        
        added_player = gs.add_player('XXX')
        added_player2 = gs.add_player('YYY')
        
        assert added_player.symbol == 'O'
        assert added_player2.symbol == 'X'