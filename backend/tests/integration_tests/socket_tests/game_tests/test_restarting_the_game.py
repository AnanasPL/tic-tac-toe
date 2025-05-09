import pytest

from ....fixtures import client_maker
from ..socket_setup_teardown import SocketSetupTeardown
from .. import set_up_the_room
from event_handlers.shared import rooms


class TestRestartingTheGame(SocketSetupTeardown):
    def test_restart_request_from_the_first_player(self, client_maker):
        code, client, client2 = set_up_the_room(client_maker, 2)
        
        client.emit('restart-request')
        
        events = client.get_received()
        events2 = client2.get_received()
        
        assert events[5]['name'] == 'play-again-state-update'
        assert events2[3]['name'] == 'play-again-state-update'
        assert events[5]['args'][0] == rooms.get_room_by_code(code).game_state.play_again_state
        assert events2[3]['args'][0] == rooms.get_room_by_code(code).game_state.play_again_state
    
    def test_restart_request_from_the_second_player(self, client_maker):
        code, client, client2 = set_up_the_room(client_maker, 2)
        
        client2.emit('restart-request')
        
        events = client.get_received()
        events2 = client2.get_received()
        
        assert events[5]['name'] == 'play-again-state-update'
        assert events2[3]['name'] == 'play-again-state-update'
        assert events[5]['args'][0] == rooms.get_room_by_code(code).game_state.play_again_state
        assert events2[3]['args'][0] == rooms.get_room_by_code(code).game_state.play_again_state
        
    def test_restart_the_game(self, client_maker):
        code, client, client2 = set_up_the_room(client_maker, 2)
        
        client.emit('restart-request')
        client2.emit('restart-request')
        
        events = client.get_received()
        events2 = client2.get_received()
        
        assert events[7]['name'] == 'board-update'
        assert events[7]['args'][0] == rooms.get_room_by_code(code).game_state.get_board_state()
        assert events[8]['name'] == 'game-restarted'

        assert events2[5]['name'] == 'board-update'
        assert events2[5]['args'][0] == rooms.get_room_by_code(code).game_state.get_board_state()
        assert events2[6]['name'] == 'game-restarted'