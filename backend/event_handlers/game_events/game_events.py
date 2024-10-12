from flask import request
from flask_socketio import emit

from event_handlers.shared import rooms

class GameEvents:
    def __init__(self, socketio) -> None:
        self.socketio = socketio
        self.register_events()
        
    def register_events(self) -> None:
        @self.socketio.on('board-update')
        def board_update(data):
            room = rooms.get_player_room(request.sid)
            
            print(data)
            room.game_state.update_board_state(data['changedCell']['index'], request.sid)
            emit('board-update', data, to=room.code)
            
            winner = room.game_state.check_for_game_end()
            
            if winner:
                emit('game-ended', winner, to=room.code)
               
        @self.socketio.on('restart-request')
        def restart_request():
            room = rooms.get_player_room(request.sid)
            room.game_state.player_wants_to_play_again(request.sid)
            
            player_symbol = room.game_state.players[request.sid]['symbol']

            emit('restart-request', {'symbol': player_symbol}, to=room.code)
            
            # If both players want to restart the game
            if not room.game_state.restart_game():
                return
            
            emit('player-info', room.game_state.get_player_info(request.sid))
            emit('player-info', room.game_state.get_opposing_player_info(request.sid), to=room.code, include_self=False)
            emit('board-clear', to=room.code)
            emit('game-restarted', to=room.code)