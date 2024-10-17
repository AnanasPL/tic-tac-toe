import pytest

from rooms import Room
from errors import *


class TestPlayerManagement:
    
    def test_add_player(self):
        r = Room()
        r.add_player('XXX')
    
        assert 'XXX' in r.get_players_session_ids()
        
    def test_add_player_room_full(self):
        r = Room()
        r.add_player('XXX')
        r.add_player('YYY')

        with pytest.raises(RoomAlreadyFullError):
            r.add_player('ZZZ')
            
    def test_remove_player(self):
        r = Room()
        r.add_player('XXX')
        r.add_player('YYY')
        
        r.remove_player('XXX')
        assert 'XXX' not in r.get_players_session_ids()
    
    def test_remove_not_existing_player(self):
        r = Room()
        
        with pytest.raises(PlayerNotFoundError):
            r.remove_player('XXX')
            
    def test_get_size(self):
        r = Room()
        r.add_player('XXX')
        r.add_player('YYY')
        
        assert r.get_size() == 2

    def test_get_players_session_ids(self):
        r = Room()
        r.add_player('XXX')
        r.add_player('YYY')
        
        assert all(sid in ('XXX', 'YYY') for sid in r.get_players_session_ids())
        
    def test_is_player_in_the_room(self):
        r = Room()
        r.add_player('XXX')
        
        assert r.is_player_in_the_room('XXX')
        assert not r.is_player_in_the_room('YYY')
