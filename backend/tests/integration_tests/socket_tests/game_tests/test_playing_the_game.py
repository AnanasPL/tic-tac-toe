import pytest

from ....fixtures import client_maker
from ..socket_setup_teardown import SocketSetupTeardown
from .. import set_up_the_room
from event_handlers.shared import rooms


class TestPlayingTheGame(SocketSetupTeardown):
    def test_update_board_correctly_first_player(self, client_maker):
        code, client, _ = set_up_the_room(client_maker, 2)
        
        client.emit('board-update', 0)
        
        assert rooms.get_room_by_code(code).game_state.get_board_state()[0] == 'O'
    
    def test_update_board_correctly_second_player(self, client_maker):
        code, client, client2 = set_up_the_room(client_maker, 2)
        
        client.emit('board-update', 0)
        client2.emit('board-update', 1)
        
        assert rooms.get_room_by_code(code).game_state.get_board_state()[1] == 'X'    

    def test_update_board_game_not_started(self, client_maker):
        _, client = set_up_the_room(client_maker)
        
        client.emit('board-update', 0)
        
        assert client.get_received()[-1]['args'][0] == "Wait for the other player"
        
    def test_update_board_turn_error(self, client_maker):
        *_, client2 = set_up_the_room(client_maker, 2)

        client2.emit('board-update', 0)
        
        assert client2.get_received()[3]['args'][0] == "Wait for your turn"

    def test_update_board_state_field_already_taken(self, client_maker):
        _, client, client2 = set_up_the_room(client_maker, 2)

        client.emit('board-update', 0)
        client2.emit('board-update', 0)
        
        assert client2.get_received()[4]['args'][0] == "This field is already taken"

    def test_game_end_tie(self, client_maker):
        _, client, client2 = set_up_the_room(client_maker, 2)
        
        client.emit('board-update', 0)
        client2.emit('board-update', 8)
        client.emit('board-update', 1)
        client2.emit('board-update', 7)
        client.emit('board-update', 6)
        client2.emit('board-update', 2)
        client.emit('board-update', 5)
        client2.emit('board-update', 3)
        client.emit('board-update', 4)
        
        assert client.get_received()[-1]['args'][0]['winner'] == 'tie'
        assert client2.get_received()[-1]['args'][0]['winner'] == 'tie'
        
    def test_game_end_winner_first_player(self, client_maker):
        _, client, client2 = set_up_the_room(client_maker, 2)
        
        client.emit('board-update', 0)
        client2.emit('board-update', 8)
        client.emit('board-update', 1)
        client2.emit('board-update', 7)
        client.emit('board-update', 2)
        
        events = client.get_received()
        events2 = client2.get_received()
                
        assert events[-1]['args'][0]['winner']
        assert not events2[-1]['args'][0]['winner']
        assert events[-1]['args'][0]['symbol'] == 'O'
        assert events2[-1]['args'][0]['symbol'] == 'O'
        
    def test_game_end_winner_second_player(self, client_maker):
        _, client, client2 = set_up_the_room(client_maker, 2)
        
        client.emit('board-update', 0)
        client2.emit('board-update', 8)
        client.emit('board-update', 1)
        client2.emit('board-update', 7)
        client.emit('board-update', 3)
        client2.emit('board-update', 6)
        
        events = client.get_received()
        events2 = client2.get_received()
          
        assert not events[-1]['args'][0]['winner']
        assert events2[-1]['args'][0]['winner']
        assert events[-1]['args'][0]['symbol'] == 'X'
        assert events2[-1]['args'][0]['symbol'] == 'X'
        