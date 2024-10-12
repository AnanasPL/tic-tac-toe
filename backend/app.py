from flask import Flask, request
from flask_socketio import SocketIO, emit

from event_handlers import GameEvents, RoomEvents
from event_handlers.shared import rooms

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

room_events = RoomEvents(socketio)
game_events = GameEvents(socketio)

#TODO: better room joining - if one player leaves the other can continue
#TODO: error handling

@socketio.on('connect')
def connect():
    emit('rooms-update', {'rooms':rooms.get_rooms_info()}, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    try:
        room = rooms.get_player_room(request.sid)
        
        room.remove_player(request.sid)
    except KeyError:
        return

if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)
    