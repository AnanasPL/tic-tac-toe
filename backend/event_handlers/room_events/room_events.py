from flask import request
from flask_socketio import emit, join_room, leave_room

from rooms.player import Player
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
        def check_if_room_exists(code: int):            
            emit('check-if-room-exists-response', code in rooms.get_all_codes())
        
        @self.socketio.on('create-room')
        def create_room_():
            room = Room()
            
            rooms.add_rooms(room)
            
            emit('room-created-successfully', room.code)
            emit('rooms-update', {'rooms': rooms.get_rooms_info()}, broadcast=True)

        @self.socketio.on('join-room')
        def join_room_(code: int):
            room = rooms.get_room_by_code(code)
            
            try:
                room.add_player(request.sid)
                join_room(code)
            except RoomAlreadyFullError:
                emit('room-already-full')
                return
            # TODO: cache (rejoining room)
            
            emit('rooms-update', {'rooms': rooms.get_rooms_info()}, broadcast=True)
            emit('board-update', room.game_state.get_board_state())
                     
            if (winner := room.game_state.get_winner()) is not None:
                if not isinstance(winner, Player):
                    emit('game-ended', {'winner': winner})
                    return
                
                symbol = room.game_state.get_player_by_session_id(request.sid).symbol
                emit('game-ended', {'winner': winner.symbol == symbol, 'symbol': winner.symbol})

        @self.socketio.on('leave-room')
        def leave_room_(code: int):
            leave_room(code)
            room = rooms.get_room_by_code(code)
            room.remove_player(request.sid)
            
            emit('rooms-update', {'rooms': rooms.get_rooms_info()}, broadcast=True)
