from typing import Union
from .board import Board


class GameState:
    def __init__(self) -> None:
        self.board = Board()
        self.players = {}
        # {
        #   session_id: {
        #         symbol: str,
        #         isCurrentPlayer: bool
        #         wantsToPlayAgain: bool | None
        #   }  
        # }
        
    def _check_for_player(self, player_sid: str):
        if player_sid not in self.players.keys():
            raise KeyError(f"There is no player with the session id of '{player_sid}' in the room")
        
    def add_player(self, player_sid: str) -> dict:
        """Adds player to the game

        Args:
            player_sid (str): Session id of the player
            
        Raises:
            KeyError: If the player is already in the players dictionary

        Returns:
            dict: 
                The added player state 
                ({'symbol': str, 'isCurrentPlayer': bool})
        """
        
        if len(self.players) > 2:
            raise ValueError("There can be at most 2 players in the room") # TODO: spectating
        
        self.players[player_sid] = {
            'symbol': 'O' if len(self.players) == 0 else 'X',
            'isCurrentPlayer':  len(self.players) == 0,
            'wantsToPlayAgain': None
        }
        
        return self.players[player_sid]
        
    def remove_player(self, player_sid: str) -> dict:
        """Removes player of the given sid from the game

        Args:
            player_sid (str): Session id of the player to be removed

        Raises:
            KeyError: If there is no player with the given id in the game

        Returns:
            dict: The player state for the removed player
        """
        
        if player_sid not in self.players.keys():
            raise KeyError(f"There is no player with the {player_sid} in the game")

        return self.players.pop(player_sid)
            
    def update_board_state(self, index: int, player_sid: str) -> None:
        """Updates the current board state.

        Args:
            index (int): Index of the cell to change. Must be between 0 and 8
            player_sid (str): Session id of the player that made a move

        Raises:
            KeyError: If there player with the given sid is not in the players dict.
            IndexError: _description_

        Returns:
            list: Updated board state.
        """
        
        self._check_for_player(player_sid)
        
        if not self.players[player_sid]['isCurrentPlayer']:
            raise PermissionError(f"It is not turn of the player with the session id of {player_sid}")
        
        symbol = self.players[player_sid]['symbol']
        
        self.board.update(index, symbol)
        self._change_turn()
    
    def _change_turn(self) -> None:
        for player_sid, player_state in self.players.items():
            self.players[player_sid]['isCurrentPlayer'] = not player_state['isCurrentPlayer']
            
    def get_winner(self) -> Union[None, dict]:
        return self.board.get_winner()
    
    def player_wants_to_play_again(self, player_sid: str, decision: bool) -> None:
        self._check_for_player(player_sid)
        
        self.players[player_sid]['wantsToPlayAgain'] = decision
    
    def get_player_info(self, player_sid: str) -> dict:
        self._check_for_player(player_sid)
        
        return self.players[player_sid]
    
    def get_opposing_player_info(self, player_sid) -> dict:
        for sid, info in self.players.items():
            if sid == player_sid:
                continue
            
            return info
    
    def all_players_want_to_play_again(self) -> bool:
        return all([player['wantsToPlayAgain'] for player in self.players.values()])
    
    def restart_game(self) -> bool:
        self.board.clear()
          
        for player, info in self.players.items():
            self.players[player]= {
                'symbol': 'O' if info['symbol'] == 'X' else 'X',
                'isCurrentPlayer': info['symbol'] == 'X',
                'wantsToPlayAgain': None
                }
    
        return True
    
    def get_board_state(self) -> list:
        return self.board.get_state()