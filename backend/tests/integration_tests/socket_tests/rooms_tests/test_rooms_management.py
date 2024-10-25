import pytest

from ....fixtures import client_maker
from ..socket_setup_teardown import SocketSetupTeardown
from event_handlers.shared import rooms


class TestRooms(SocketSetupTeardown):
    def test_room_created_successfully(self, client_maker):
        client = client_maker()
        
        client.emit('create-room')
        
        code = client.get_received()[1]['args'][0]
        
        assert rooms.get_room_by_code(code)
        
    def test_create_and_join_room(self, client_maker):
        client = client_maker()
        
        client.emit('create-room')
        
        code = client.get_received()[1]['args'][0]
        
        client.emit('join-room', code)
        print(rooms.get_all_players_session_ids())
        assert len(rooms.get_all_players_session_ids()) == 1
        
    def test_create_join_and_leave_room(self, client_maker):
        client = client_maker()
        
        client.emit('create-room')
        
        code = client.get_received()[1]['args'][0]
        
        client.emit('join-room', code)
        client.emit('leave-room', code)
        
        assert len(rooms.get_all_players_session_ids()) == 0
        
    def test_remove_empty_rooms(self, client_maker):
        client = client_maker()
        client2 = client_maker()
        
        client.emit('create-room')
        client.emit('remove-empty-rooms')

        assert len(rooms._rooms) == 0
        assert client.get_received()[1]['name'] == 'rooms-update'
        assert client2.get_received()[1]['name'] == 'rooms-update'
        
    def test_room_exists(self, client_maker):
        client = client_maker()
        
        client.emit('create-room')
    
        code = client.get_received()[1]['args'][0]
        
        client.emit('check-if-room-exists', code)
        client.emit('check-if-room-exists', '-----')
        
        events = client.get_received()
        
        assert events[0]['args'][0]
        assert not events[1]['args'][0]

    def test_join_full_room(self, client_maker):
        client = client_maker()
        client2 = client_maker()
        client3 = client_maker()
        
        client.emit('create-room')
        
        code = client.get_received()[3]['args'][0]
        
        client.emit('join-room', code)
        client2.emit('join-room', code)
        client3.emit('join-room', code)
        
        assert rooms.all_rooms_full()
        assert len(rooms._rooms) == 1
        assert client3.get_received()[-1]['name'] == 'room-already-full'