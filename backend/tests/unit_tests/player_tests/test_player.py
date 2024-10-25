import pytest

from rooms.player import Player


class TestPlayer:
    def test_compare_players_true(self):
        assert Player('XXX', 'X') == Player('XXX', 'O') 
    
    def test_compare_players_false(self):
        assert Player('YYY', 'X') != Player('XXX', 'O') 
    
    @pytest.mark.parametrize('object_to_compare', [1234, True, 'XXX', 3.14, None, (), {}, []])
    def test_compare_player_and_other_object(self, object_to_compare):
        assert Player('XXX', 'X') != object_to_compare
    
    def test_compare_hashes(self):
        assert Player('XXX', 'X', True).__hash__() == Player('XXX', 'O', False).__hash__() 
        
    @pytest.mark.parametrize('symbol, opposite_symbol', [('O', 'X'), ('X', 'O')])
    def test_reverse_symbol(self, symbol, opposite_symbol):
        player = Player('XXX', symbol)
        player.reverse_symbol()
        
        assert player.symbol == opposite_symbol
        
    def test_change_turn(self):
        player = Player('XXX', 'O')
        player2 = Player('YYY', 'X')
        
        player.change_turn()
        player2.change_turn()
        
        assert not player.is_current_player
        assert player2.is_current_player
    
    def test_determine_turn_at_the_start(self):
        player = Player('XXX', 'O')
        player2 = Player('YYY', 'X')
        
        assert player.is_current_player 
        assert not player2.is_current_player 
        
    @pytest.mark.parametrize('symbol, is_current_player, wants_to_play_again', [
        ('O', True, None),
        ('O', True, False),
        ('O', True, True),
        ('X', False, None),
        ('X', False, False),
        ('X', False, True)
    ])
    def test_get_player_state_returns_correct_state(self, symbol, is_current_player, wants_to_play_again):
        player = Player('XXX', symbol, wants_to_play_again=wants_to_play_again)
        
        assert player.get_state() == {
            'symbol': symbol,
            'isCurrentPlayer': is_current_player, 
            'wantsToPlayAgain': wants_to_play_again, 
        }