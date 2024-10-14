from typing import Union


class Player:
    """A player in Tic-Tac-Toe game
    
    Attributes: 
        session_id (str): A session id of the player
        symbol (str): A symbol of the player. Should be `O` or `X`
        is_current_player (bool): Whether the player is able to make a move now
        wants_to_play_again (None | bool): 
            Whether the player wants to play again or not,
            or is the decision unmade
    """
    
    def __init__(
        self, 
        session_id: str,
        symbol: str, 
        wants_to_play_again: Union[None, bool] = None
        ) -> None:
        """    
        Args: 
            session_id (str): A session id of the player
            symbol (str): A symbol of the player. Should be `O` or `X`
            wants_to_play_again (None | bool): 
                Whether the player wants to play again or not,
                or is the decision unmade. None by default
        """
        self.session_id = session_id       
        self.symbol = symbol
        self.determine_turn_at_the_start()
        self.wants_to_play_again = wants_to_play_again
        
    def __eq__(self, other: object) -> bool:
        """
        Returns `True` if the session_id of the other player is equal, 
        `False` otherwise or if the compared object is not an instance of Player
        """
        if isinstance(other, Player):
            return self.session_id == other.session_id
        
        return False
    
    def __hash__(self) -> int:
        return hash(self.session_id)
        
    def reverse_symbol(self) -> str:
        """
        Toggles between 'X' and 'O' symbols and returns the updated symbol.
        
        Returns:
            str: The new value of `symbol`.
        """
        self.symbol = 'O' if self.symbol == 'X' else 'X'
        
        return self.symbol
        
    def change_turn(self) -> bool:
        """Changes the `is_current_player` attribute to the opposite.
        
        Returns:
            bool: The new `is_current_player` value
        """
        self.is_current_player = not self.is_current_player
        
        return self.is_current_player
    
    def get_state(self) -> dict:
        """Returns the current player state, as a dictionary
        
        Returns:
            dict: 
                The player state.
                `{'symbol': str, 'isCurrentPlayer': bool, 'wantsToPlayAgain': bool}`
        """
        
        return {
            'symbol': self.symbol,
            'isCurrentPlayer': self.is_current_player,
            'wantsToPlayAgain': self.wants_to_play_again,
        }

    def determine_turn_at_the_start(self) -> bool:
        """
        Sets the `is_current_player` depending on the `symbol` property.
        True if `O`, false otherwise 
        """
        self.is_current_player = self.symbol == 'O'
        
        return self.is_current_player
