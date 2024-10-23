import pytest
from flask_socketio import SocketIOTestClient

from app import app, socketio


@pytest.fixture
def client_maker():
    clients = set()
    
    def create_client() -> SocketIOTestClient:
        app.config['TESTING'] = True
        
        return socketio.test_client(app)
        
    yield create_client
        
    for client in clients:
        client.disconnect()
