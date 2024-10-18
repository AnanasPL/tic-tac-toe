import pytest

from app import app, socketio

@pytest.fixture
def client():
    app.config['TESTING'] = True  
    app.config['SECRET_KEY'] = 'testsecret'  
    
    client = socketio.test_client(app)
    
    yield client
    
    client.disconnect()
