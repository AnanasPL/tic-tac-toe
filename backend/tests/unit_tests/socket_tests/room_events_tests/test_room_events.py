import pytest 

from ..test_client import client


def check_response(events: object, length: int, index: int, name: str, argname: str, type_: object):
    assert len(events) == length
    assert events[index]['name'] == name
    assert isinstance(events[index]['args'][0][argname], type_)


class TestRoomEvents:
    def test_get_rooms(self, client):
        client.emit('get-rooms')
        events = client.get_received()
        
        check_response(events, 2, 1, 'rooms-update', 'rooms', list)
        
    def test_remove_empty_rooms(self, client):
        client.emit('remove-empty-rooms')
        events = client.get_received()
        
        check_response(events, 2, 1, 'rooms-update', 'rooms', list)
    
    def test_check_if_room_exists(self, client):
        client.emit('check-if-room-exists', {'code': 'XXXXXX'})
        events = client.get_received()
        
        check_response(events, 2, 1, 'check-if-room-exists-response', 'exists', bool)

    def test_create_room(self, client):
        client.emit('create-room')
        events = client.get_received()
        
        check_response(events, 3, 1, 'room-created-successfully', 'code', str)
        check_response(events, 3, 2, 'rooms-update', 'rooms', list)

