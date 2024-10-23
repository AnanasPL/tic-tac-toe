import pytest

from rooms.gamestate import GameState
from errors import *

from ...fixtures import gs

class TestUpdateState:
    def test_update_board_state_game_not_started(self):
        gs = GameState()
        gs.add_player('XXX')
        
        with pytest.raises(GameHasNotStartedError):
            gs.update_board_state(0, 'XXX')    
    
    @pytest.mark.parametrize('index', [-1, 9])
    def test_update_board_state_invalid_index(self, gs, index):
        with pytest.raises(IndexError):
            gs.update_board_state(index, 'XXX')
        
    def test_update_board_state_invalid_player_session_id(self, gs):
        with pytest.raises(PlayerNotFoundError):
            gs.update_board_state(0, 'ZZZ')
            
    def test_update_board_state_already_taken_field(self, gs):
        gs.update_board_state(0, 'XXX')
        
        with pytest.raises(FieldAlreadyTakenError):
            gs.update_board_state(0, 'YYY')
            
    def test_update_board_state_wrong_player_at_the_start(self, gs):
        with pytest.raises(TurnError):
            gs.update_board_state(0, 'YYY')
            
    def test_update_board_state_wrong_player_after_turn_change(self, gs):
        gs.update_board_state(0, 'XXX')
        
        with pytest.raises(TurnError):
            gs.update_board_state(1, 'XXX')
    
    @pytest.mark.parametrize('index', [i for i in range(9)])
    def test_update_board_state(self, index, gs):
        gs.update_board_state(index, 'XXX')
        
        assert gs.get_board_state()[index] == 'O'
        
    def test_turn_changed_properly_after_first_update(self, gs):
        gs.update_board_state(0, 'XXX')
        
        assert not gs.get_player_info('XXX')['isCurrentPlayer']
        assert gs.get_opposing_player_info('XXX')['isCurrentPlayer']
        
    def test_turn_changed_properly_after_second_update(self, gs):
        gs.update_board_state(0, 'XXX')
        gs.update_board_state(1, 'YYY')
        
        assert gs.get_player_info('XXX')['isCurrentPlayer']
        assert not gs.get_opposing_player_info('XXX')['isCurrentPlayer']