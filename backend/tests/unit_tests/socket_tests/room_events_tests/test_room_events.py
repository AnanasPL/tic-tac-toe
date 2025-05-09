import pytest 

from typing import Union

from ....fixtures.client import client_maker


def check_response(events: object, length: int, index: int, name: str, argname: Union[str, None], type_: object):
    assert len(events) == length
    assert events[index]['name'] == name
    
    if argname is None:
        assert isinstance(events[index]['args'][0], type_)
    else:
        assert isinstance(events[index]['args'][0][argname], type_)


class TestRoomEvents:
    def test_get_rooms(self, client_maker):
        client = client_maker()
        
        client.emit('get-rooms')
        events = client.get_received()
        
        check_response(events, 2, 1, 'rooms-update', 'rooms', list)
        
    def test_remove_empty_rooms(self, client_maker):
        client = client_maker()
        
        client.emit('remove-empty-rooms')
        events = client.get_received()
        
        check_response(events, 2, 1, 'rooms-update', 'rooms', list)
    
    def test_check_if_room_exists(self, client_maker):
        client = client_maker()
        
        client.emit('check-if-room-exists', 'XXXXXX')
        events = client.get_received()
        
        check_response(events, 2, 1, 'check-if-room-exists-response', None, bool)

    def test_create_room(self, client_maker):
        client = client_maker()
        
        client.emit('create-room')
        events = client.get_received()
        
        check_response(events, 3, 1, 'room-created-successfully', None, str)
        check_response(events, 3, 2, 'rooms-update', 'rooms', list)
