import pytest 

from ....fixtures.client import client_maker

class TestConnection:
    def test_connect(self, client_maker):
        client = client_maker()
        events = client.get_received()
        
        assert len(events) == 1
        assert events[0]['name'] == 'rooms-update'
        assert events[0]['args'][0]['rooms'] == []
        