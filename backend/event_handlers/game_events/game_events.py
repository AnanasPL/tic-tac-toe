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
                
        @self.socketio.on('game-restart')
        def restart_game():
            print('restart request from', request.sid)
            room = rooms.get_player_room(request.sid)
            room.game_state.player_wants_to_play_again(request.sid)
            
            if not room.game_state.restart_game():
                return
            
            for player, info in room.game_state.players.items():
                if player == request.sid:
                    player_state = info
                else:
                    player_state2 = info
            
            print('info sent to player one', player_state)
            print('info sent to player two', player_state2)
            
            emit('player-info', player_state)
            emit('player-info', player_state2, to=room.code, include_self=False)
            emit('board-clear', to=room.code)
            emit('game-restarted', to=room.code)
