import pytest 

from ..test_client import client

class TestConnection:
    def test_connect(self, client):
        events = client.get_received()
        
        assert len(events) == 1
        assert events[0]['name'] == 'rooms-update'
        assert events[0]['args'][0]['rooms'] == []
        

        