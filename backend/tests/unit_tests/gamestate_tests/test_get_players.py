import pytest

from rooms.gamestate import GameState
from errors import *

class TestGetPlayerFromTheGameState:
    def test_getting_player_by_session_id(self):
        gs = GameState()
        added_player = gs.add_player('XXX')
        
        assert gs.get_player_by_session_id('XXX') is added_player
    
    def test_get_player_by_symbol(self):
        gs = GameState()
        added_player = gs.add_player('XXX')
        
        assert gs.get_player_by_symbol('O') is added_player
    
    def test_get_player_by_symbol_invalid_symbol(self):
        gs = GameState()
        gs.add_player('XXX')
        
        with pytest.raises(PlayerNotFoundError):
            gs.get_player_by_symbol('-')
     
    def test_getting_player_by_session_id_invalid_session_id(self):
        gs = GameState()
        gs.add_player('XXX')
        
        with pytest.raises(PlayerNotFoundError):
            gs.get_player_by_session_id('YYY')
            
    def test_getting_all_session_ids(self):
        gs = GameState()
        gs.add_player('XXX')
        gs.add_player('YYY')
        
        assert all(sid in ('XXX', 'YYY') for sid in gs.get_players_session_ids())
        
    def test_get_player_info(self):
        gs = GameState()
        gs.add_player('XXX')
        
        assert gs.get_player_info('XXX') == {
            'symbol': 'O', 
            'isCurrentPlayer': True,
            }
    
    def test_get_opposing_player_info(self):
        gs = GameState()
        gs.add_player('XXX')
        gs.add_player('YYY')
        
        assert gs.get_opposing_player_info('XXX') == {
            'symbol': 'X', 
            'isCurrentPlayer': False,
            }

    def test_get_opposing_player_info_when_there_is_only_one_player(self):
        gs = GameState()
        gs.add_player('XXX')
        
        assert gs.get_opposing_player_info('XXX') is None