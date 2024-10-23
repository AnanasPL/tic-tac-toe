from flask import request
from flask_socketio import emit 

from rooms.player import Player

from event_handlers.shared import rooms
from ..event_handler import EventHandler
from errors import *

class GameEvents(EventHandler):        
    def register_events(self) -> None:
        @self.socketio.on('board-update')
        def board_update(data):
            #TODO: go from sending dicts to sending single args. will be easier
            room = rooms.get_player_room(request.sid)
            
            error_message = ''
            try:
                room.game_state.update_board_state(data['changedCell']['index'], request.sid)
            except GameHasNotStartedError:
                error_message = "The game has not started yet"
            except TurnError:
                error_message = "Wait for your turn"
            except FieldAlreadyTakenError:
                error_message = "This field is already taken"
            finally:
                if error_message:
                    emit('board-update-error', {'message': error_message})
                    return
            #TODO: fix update sending, send entire board state instead of one cell
            emit('board-update', data, to=room.code)
            
            winner = room.game_state.get_winner()
            
            # TODO: change the thing to send personalized event to each player
            # instead of sending symbol as the client should not know its symbol
            if winner is not None:
                if isinstance(winner, Player):
                    winner = winner.symbol
                
                emit('game-ended', {'winner': winner}, to=room.code)
               
        @self.socketio.on('restart-request')
        def restart_request():
            room = rooms.get_player_room(request.sid)
            room.game_state.player_wants_to_play_again(request.sid, True)
            
            player_symbol = room.game_state.get_player_by_session_id(request.sid).symbol

            emit('restart-request', {'symbol': player_symbol}, to=room.code)
            
            # If both players want to restart the game
            if room.game_state.all_players_want_to_play_again():
                room.game_state.restart_game() 
                
                emit('player-info', room.game_state.get_player_info(request.sid))
                emit('player-info', room.game_state.get_opposing_player_info(request.sid), to=room.code, skip_sid=request.sid)
                emit('board-clear', to=room.code)
                emit('game-restarted', to=room.code)
                
                #TODO: in board update, send back message if the move is invalid