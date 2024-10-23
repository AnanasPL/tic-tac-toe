import pytest

from errors import *

from ...fixtures import rooms


class TestGetRoomsInfo:
    def test_get_room_codes(self, rooms):
        r, room, room2 = rooms
        
        assert all(code in (room.code, room2.code) for code in r.get_all_codes())
        
    def test_get_all_players_session_ids(self, rooms):
        r, room, room2 = rooms
        
        room.add_player('XXX')
        room2.add_player('YYY')
        
        assert all(sid in ('XXX', 'YYY') for sid in r.get_all_players_session_ids())
        
    def test_get_first_available_room(self, rooms):
        r, room, room2 = rooms
        
        room.add_player('XXX')
        room.add_player('YYY')
        room2.add_player('ZZZ')
        
        assert r.get_first_available_room() is room2
        
    def test_get_first_available_room_when_there_is_not_any(self, rooms):
        r, room, room2 = rooms
        
        room.add_player('XXX')
        room.add_player('YYY')
        room2.add_player('ZZZ')
        room2.add_player('VVV')
        
        assert r.get_first_available_room() is None
    
    def test_all_rooms_full(self, rooms):
        r, room, room2 = rooms
        
        room.add_player('XXX')
        room.add_player('YYY')
        room2.add_player('ZZZ')
        
        assert not r.all_rooms_full()        
        
        room2.add_player('VVV')
        
        assert r.all_rooms_full()
        
    def test_get_player_room(self, rooms):
        r, room, _ = rooms
        
        room.add_player('XXX')
        
        assert r.get_player_room('XXX') is room
        
    def test_get_player_room_invalid_player(self, rooms):
        r, room, _ = rooms
        
        room.add_player('XXX')
        
        with pytest.raises(PlayerNotFoundError):
            r.get_player_room('ZZZ')
    
    def test_get_room_by_code(self, rooms):
        r, room, _ = rooms
        
        assert r.get_room_by_code(room.code) is room
        
    def test_get_room_by_code_invalid_code(self, rooms):
        r, *_ = rooms
        
        with pytest.raises(RoomNotFoundError):
            r.get_room_by_code('-----')
            
    def test_get_rooms_info(self, rooms):
        r, room, room2 = rooms
        
        room.add_player('XXX')
        room.add_player('YYY')
        room2.add_player('ZZZ')
        
        assert sorted(r.get_rooms_info()) == sorted(((room.code, 2), (room2.code, 1)))