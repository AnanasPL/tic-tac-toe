import pytest

from ....fixtures import client_maker
from ..socket_setup_teardown import SocketSetupTeardown
from .. import set_up_the_room
from event_handlers.shared import rooms


class TestRestartingTheGame(SocketSetupTeardown):
    def test_restart_request_from_the_first_player(self, client_maker):
        _, client, client2 = set_up_the_room(client_maker, 2)
        
        client.emit('restart-request')
        
        events = client.get_received()
        events2 = client2.get_received()
        
        assert events[6]['name'] == 'restart-request'
        assert events2[4]['name'] == 'restart-request'
        assert events[6]['args'][0]['symbol'] == 'O'
        assert events2[4]['args'][0]['symbol'] == 'O'
    
    def test_restart_request_from_the_second_player(self, client_maker):
        _, client, client2 = set_up_the_room(client_maker, 2)
        
        client2.emit('restart-request')
        
        events = client.get_received()
        events2 = client2.get_received()
        
        assert events[6]['name'] == 'restart-request'
        assert events2[4]['name'] == 'restart-request'
        assert events[6]['args'][0]['symbol'] == 'X'
        assert events2[4]['args'][0]['symbol'] == 'X'
        
    def test_restart_the_game(self, client_maker):
        code, client, client2 = set_up_the_room(client_maker, 2)
        
        client.emit('restart-request')
        client2.emit('restart-request')
        
        events = client.get_received()
        events2 = client2.get_received()
        
        assert events[8]['name'] == 'player-info'
        assert events[8]['args'][0] == {'symbol': 'X', 'isCurrentPlayer': False, 'wantsToPlayAgain': None}
        assert events[9]['name'] == 'board-update'
        assert events[9]['args'][0] == rooms.get_room_by_code(code).game_state.get_board_state()
        assert events[10]['name'] == 'game-restarted'
        
        assert events2[6]['name'] == 'player-info'
        assert events2[6]['args'][0] == {'symbol': 'O', 'isCurrentPlayer': True, 'wantsToPlayAgain': None}
        assert events2[7]['name'] == 'board-update'
        assert events2[7]['args'][0] == rooms.get_room_by_code(code).game_state.get_board_state()
        assert events2[8]['name'] == 'game-restarted'