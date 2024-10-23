from flask import request
from flask_socketio import emit, join_room, leave_room

from rooms import Room
from event_handlers.shared import rooms
from ..event_handler import EventHandler

from errors import *

class RoomEvents(EventHandler):        
    def register_events(self) -> None:
        @self.socketio.on('get-rooms')
        def get_rooms():
            emit('rooms-update', {'rooms': rooms.get_rooms_info()})
            
        @self.socketio.on('remove-empty-rooms')
        def clear_empty_rooms():
            rooms.remove_empty_rooms()
            
            emit('rooms-update', {'rooms': rooms.get_rooms_info()}, broadcast=True)
            
        @self.socketio.on('check-if-room-exists')
        def check_if_room_exists(data):
            code = data['code']
            
            emit('check-if-room-exists-response', {'exists': code in rooms.get_all_codes()})
        
        @self.socketio.on('create-room')
        def create_room_():
            room = Room()
            
            rooms.add_rooms(room)
            
            emit('room-created-successfully', {'code': room.code})
            emit('rooms-update', {'rooms': rooms.get_rooms_info()}, broadcast=True)

        @self.socketio.on('join-room')
        def join_room_(data):
            code = data['code']
            
            room = rooms.get_room_by_code(code)
            
            try:
                player = room.add_player(request.sid)
                join_room(code)
            except RoomAlreadyFullError:
                emit('room-already-full')
                return
                
            emit('rooms-update', {'rooms': rooms.get_rooms_info()}, broadcast=True)
            emit('player-info', player.get_state())

        @self.socketio.on('leave-room')
        def leave_room_(data):
            code = data['code']
            
            leave_room(code)
            room = rooms.get_room_by_code(code)
            room.remove_player(request.sid)
            
            emit('rooms-update', {'rooms': rooms.get_rooms_info()}, broadcast=True)
