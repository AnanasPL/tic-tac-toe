from flask import request
from flask_socketio import emit 

from rooms.player import Player

from event_handlers.shared import rooms
from ..event_handler import EventHandler
from errors import *

class GameEvents(EventHandler):        
    def register_events(self) -> None:
        @self.socketio.on('board-update')
        def board_update(index: int):
            #TODO: go from sending dicts to sending single args. will be easier
            room = rooms.get_player_room(request.sid)
            
            error_message = ''
            try:
                room.game_state.update_board_state(index, request.sid)
            except NotEnoughPlayersError:
                error_message = "Wait for the other player"
            except TurnError:
                error_message = "Wait for your turn"
            except FieldAlreadyTakenError:
                error_message = "This field is already taken"
            finally:
                if error_message:
                    emit('board-update-error', error_message)
                    return

            emit('board-update', room.game_state.get_board_state(), to=room.code)
            
            if (winner := room.game_state.get_winner()) is not None:
                if not isinstance(winner, Player):
                    emit('game-ended', {'winner': winner}, to=room.code)
                    return
                    
                emit('game-ended', {'winner': True, 'symbol': winner.symbol}, to=winner.session_id)
                emit('game-ended', {'winner': False, 'symbol': winner.symbol}, to=room.code, skip_sid=winner.session_id)
               
        @self.socketio.on('restart-request')
        def restart_request():
            room = rooms.get_player_room(request.sid)
            room.game_state.player_wants_to_play_again(request.sid, True)
            
            player_symbol = room.game_state.get_player_by_session_id(request.sid).symbol

            emit('restart-request', {'symbol': player_symbol}, to=room.code)
            
            # If both players want to restart the game
            if room.game_state.all_players_want_to_play_again():
                room.game_state.restart_game() 

                emit('board-update', room.game_state.get_board_state(), to=room.code)
                emit('game-restarted', to=room.code)
                