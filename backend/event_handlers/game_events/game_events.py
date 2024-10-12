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
            
            error_message = ''
            try:
                room.game_state.update_board_state(data['changedCell']['index'], request.sid)
            except PermissionError as e:
                error_message = "Poczekaj na swoją kolej"
            except ValueError:
                error_message = "Pole niedostępne"
            finally:    
                if error_message:
                    emit('board-update-error', {'message': error_message})
                    return
            
            emit('board-update', data, to=room.code)
            
            winner = room.game_state.get_winner()
            
            if winner is not None:
                emit('game-ended', {'winner': winner}, to=room.code)
               
        @self.socketio.on('restart-request')
        def restart_request():
            room = rooms.get_player_room(request.sid)
            room.game_state.player_wants_to_play_again(request.sid, True)
            
            player_symbol = room.game_state.players[request.sid]['symbol']

            emit('restart-request', {'symbol': player_symbol}, to=room.code)
            
            # If both players want to restart the game
            if room.game_state.all_players_want_to_play_again():
                room.game_state.restart_game() 
                
                emit('player-info', room.game_state.get_player_info(request.sid))
                emit('player-info', room.game_state.get_opposing_player_info(request.sid), to=room.code, include_self=False)
                emit('board-clear', to=room.code)
                emit('game-restarted', to=room.code)
                
                
                #TODO: in board update, send back message if the move is invalid