import pytest

from app import app, socketio

@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    client = socketio.test_client(app)
    
    yield client
    
    client.disconnect()
