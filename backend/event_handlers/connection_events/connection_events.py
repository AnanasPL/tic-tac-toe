from flask import request
from flask_socketio import SocketIO, emit

from event_handlers.shared import rooms

class ConnectionEvents:
    def __init__(self, socketio: SocketIO) -> None:
        self.socketio = socketio
        self.register_events()


    def register_events(self) -> None:
        @self.socketio.on('connect')
        def connect():
            emit('rooms-update', {'rooms':rooms.get_rooms_info()}, broadcast=True)

        @self.socketio.on('disconnect')
        def disconnect():
            try:
                room = rooms.get_player_room(request.sid)
                
                room.remove_player(request.sid)
            except KeyError:
                return
