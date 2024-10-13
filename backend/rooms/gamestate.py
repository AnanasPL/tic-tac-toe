from typing import Union

from errors import *
from .board import Board
from .player import Player

class GameState:   
    """Game state of a Tic-Tac-Toe game.
    
    Attributes:
        board (Board): Current board state
        players (set[Player]): List of players in the game
    """
    
    def __init__(self) -> None:
        self.board = Board()
        self.players: set[Player] = set()
                
    def get_players_session_ids(self) -> tuple[str]:
        """Returns a tuple with all the session ids of the players in the game"""
        return (player.session_id for player in self.players)   
    
    def _check_for_player(self, player_sid: str) -> None:
        """Checks if player with the given session id is in the room

        Args:
            player_sid (str): The session id of the player

        Raises:
            PlayerNotFoundError: If the player is not in the room
        """
        if player_sid not in self.get_players_session_ids():
            raise PlayerNotFoundError(f"There is no player with the session id of '{player_sid}' in the room")
        
    def get_player_by_session_id(self, player_sid: str) -> Player:
        """Returns the player object of the given player id

        Args:
            player_sid (str): The session id of the player
        
        Raises:
            PlayerNotFoundError: If the player is not in the room
        """
        self._check_for_player(player_sid)
        
        for player in self.players:
            if player.session_id == player_sid:
                return player
    
    def add_player(self, player_sid: str) -> Player:
        """Adds player to the game

        Args:
            player_sid (str): Session id of the player
            
        Returns:
            Player: The added player

        Raises:
            RoomAlreadyFullError: If the room is already full
        """
        if len(self.players) >= 2:
            raise RoomAlreadyFullError("There can be at most 2 players in the room") # TODO: spectating
        
        self.players.add(Player(
            player_sid, 
            'O' if len(self.players) == 0 else 'X',
            len(self.players) == 0,
            None
        ))
                
        return self.get_player_by_session_id(player_sid)
        
    def remove_player(self, player_sid: str) -> None:
        """Removes player of the given sid from the game

        Args:
            player_sid (str): Session id of the player to be removed

        Raises:
            PlayerNotFoundError: If the player is not in the room
        """
        player = self.get_player_by_session_id(player_sid)
        self.players.discard(player)
            
    def update_board_state(self, index: int, player_sid: str) -> None:
        """Updates the current board state.

        Args:
            index (int): Index of the cell to change. Must be between 0 and 8
            player_sid (str): Session id of the player that made a move

        Raises:
            PlayerNotFoundError: If the player is not in the room
            IndexError: If the index is out of range 0-8
            FieldAlreadyTakenError: If the field is already taken
            TurnError: If its not the turn of the player
        """
        # if len(self.players) != 2:
        #     raise er
        player = self.get_player_by_session_id(player_sid)
        
        if not player.is_current_player:
            raise TurnError(f"It is not turn of the player with the session id of {player_sid}")
        
        self.board.update(index, player.symbol)
        self._change_turn()
    
    def _change_turn(self) -> None:
        """Changes the is_current_player property to the opposite for each player"""
        for player in self.players:
            player.change_turn()
            
    def get_winner(self) -> Union[str, None]:
        """Returns the winner of the game

        Returns:
            str:
                `O` or `X` if there is a winner, and `tie` if the game has ended and
                neither of the players won
                
            None: 
                If there is no winner and the game is still in progress
        """
        return self.board.get_winner()
    
    def player_wants_to_play_again(self, player_sid: str, decision: bool) -> None:
        """Sets the wants_to_play_again property of the player with given session id

        Args:
            player_sid (str): The session id of the player
            decision (bool): Whether the player wants to play again, or not
            
        Raises:
            PlayerNotFoundError: If the player is not in the room
        """
        self.get_player_by_session_id(player_sid).wants_to_play_again = decision
    
    def get_player_info(self, player_sid: str) -> dict:
        """Returns the player state of the player with the given session id

        Args:
            player_sid (str): The session id of the player

        Returns:
            dict: 
                The player state.
                `{'symbol': str, 'isCurrentPlayer': bool, 'wantsToPlayAgain': bool}`
                
        Raises:
            PlayerNotFoundError: If the player is not in the room
        """
        return self.get_player_by_session_id(player_sid).get_state()
    
    def get_opposing_player_info(self, player_sid) -> Union[dict, None]:
        """Returns the player state of the player with the session id **other** than the given

        Args:
            player_sid (str): The session id of the player

        Returns:
            dict: 
                The opposing player state.
                `{'symbol': str, 'isCurrentPlayer': bool, 'wantsToPlayAgain': bool}`
                
            None: If the player with the given session id is the only one in the game
        """
        for player in self.players:
            if player.session_id != player_sid:
                return player.get_state()
            
    def all_players_want_to_play_again(self) -> bool:
        """Returns whether all players want to play again or not

        Returns:
            bool:
                `True` if the `wants_to_play_again` property is `True`
                for every player, False otherwise
        """
        return all([player.wants_to_play_again for player in self.players])
    
    def restart_game(self) -> None:
        """Restarts the game.
        
        Clears the board, reverses each player's symbol,
        sets `is_current_player` property to the correct one
        ("O" always starts), and sets 
        `wants_to_play_again` property back to `None` 
        """
        self.board.clear()
          
        for player in self.players:
            player.reverse_symbol()
            player.determine_turn_at_the_start()
            player.wants_to_play_again = None

    def get_board_state(self) -> list:
        """Returns the current board state

        Returns:
            list: The current board state
        """
        return self.board.get_state()