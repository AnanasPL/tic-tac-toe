import pytest

from errors import *

from ...fixtures import rooms

class TestModifyRoomsList:
    def test_add_rooms(self, rooms):
        r, room, room2 = rooms
        
        assert room in r._rooms and room2 in r._rooms
    
    def test_remove_empty_rooms(self, rooms):
        r, room, room2 = rooms
        
        room.add_player('XXX')
        
        r.remove_empty_rooms()
        
        assert room2 not in r._rooms