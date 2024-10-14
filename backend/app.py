from flask import Flask
from flask_socketio import SocketIO
from flask.testing import FlaskClient
from event_handlers import GameEvents, RoomEvents, ConnectionEvents

app = Flask(__name__).test_client()
socketio = SocketIO(app, cors_allowed_origins='*')

room_events = RoomEvents(socketio)
game_events = GameEvents(socketio)
connection_events = ConnectionEvents

if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)
    