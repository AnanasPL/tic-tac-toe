import pytest

from ....fixtures import client_maker
from ..socket_setup_teardown import SocketSetupTeardown
from .. import set_up_the_room
from event_handlers.shared import rooms


class TestPlayingTheGame(SocketSetupTeardown):
    def test_state_sent_correctly(self, client_maker):
        code, (client) = set_up_the_room(client_maker)
        state = list(rooms.get_room_by_code(code).game_state.players)[0].get_state()
        
        assert client.get_received()[-1]['args'][0] == state
    
    def test_update_board_game_not_started(self, client_maker):
        _, client = set_up_the_room(client_maker)
        
        client.emit('board-update', {'changedCell': {'index': 0, 'symbol': 'O'}})
        
        assert client.get_received()[-1]['args'][0]['message'] == "The game has not started yet"
        
    def test_update_board_turn_error(self, client_maker):
        *_, client2 = set_up_the_room(client_maker, 2)

        client2.emit('board-update', {'changedCell': {'index': 0}})
        
        assert client2.get_received()[3]['args'][0]['message'] == "Wait for your turn"

    def test_update_board_state_field_already_taken(self, client_maker):
        _, client, client2 = set_up_the_room(client_maker, 2)

        client.emit('board-update', {'changedCell': {'index': 0}})
        client2.emit('board-update', {'changedCell': {'index': 0}})
        
        assert client2.get_received()[4]['args'][0]['message'] == "This field is already taken"

    def test_game_end_tie(self, client_maker):
        _, client, client2 = set_up_the_room(client_maker, 2)
        
        client.emit('board-update', {'changedCell': {'index': 0}})
        client2.emit('board-update', {'changedCell': {'index': 8}})
        client.emit('board-update', {'changedCell': {'index': 1}})
        client2.emit('board-update', {'changedCell': {'index': 7}})
        client.emit('board-update', {'changedCell': {'index': 6}})
        client2.emit('board-update', {'changedCell': {'index': 2}})
        client.emit('board-update', {'changedCell': {'index': 5}})
        client2.emit('board-update', {'changedCell': {'index': 3}})
        client.emit('board-update', {'changedCell': {'index': 4}})
        
        assert client.get_received()[-1]['args'][0]['winner'] == 'tie'
        assert client2.get_received()[-1]['args'][0]['winner'] == 'tie'
        
    def test_game_end_winner_first_player(self, client_maker):
        _, client, client2 = set_up_the_room(client_maker, 2)
        
        client.emit('board-update', {'changedCell': {'index': 0}})
        client2.emit('board-update', {'changedCell': {'index': 8}})
        client.emit('board-update', {'changedCell': {'index': 1}})
        client2.emit('board-update', {'changedCell': {'index': 7}})
        client.emit('board-update', {'changedCell': {'index': 2}})
        
        assert client.get_received()[-1]['args'][0]['winner'] == 'O'
        assert client2.get_received()[-1]['args'][0]['winner'] == 'O'
        
    def test_game_end_winner_second_player(self, client_maker):
        _, client, client2 = set_up_the_room(client_maker, 2)
        
        client.emit('board-update', {'changedCell': {'index': 0}})
        client2.emit('board-update', {'changedCell': {'index': 8}})
        client.emit('board-update', {'changedCell': {'index': 1}})
        client2.emit('board-update', {'changedCell': {'index': 7}})
        client.emit('board-update', {'changedCell': {'index': 3}})
        client2.emit('board-update', {'changedCell': {'index': 6}})
        
        assert client.get_received()[-1]['args'][0]['winner'] == 'X'
        assert client2.get_received()[-1]['args'][0]['winner'] == 'X'
        