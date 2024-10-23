import pytest

from ....fixtures import client_maker
from ..socket_setup_teardown import SocketSetupTeardown
from .. import set_up_the_room
from event_handlers.shared import rooms

# Note: test_connect already in the unit tests 
class TestConnectionEvents(SocketSetupTeardown):
    def test_disconnect(self, client_maker):
        code, client, client2 = set_up_the_room(client_maker, 2)
        client3 = client_maker()
        
        client.disconnect(), client2.disconnect()
        
        events = client3.get_received()
        
        assert len(events) == 3
        assert events[1]['args'][0]['rooms'][0] == [code, 1]
        assert events[2]['args'][0]['rooms'][0] == [code, 0]
        assert rooms._rooms[0].get_size() == 0