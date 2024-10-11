from typing import Union


class GameState:
    def __init__(self) -> None:
        self.board_state = ['' for _ in range(9)]
        self.players = {}
        self.game_ended = False
        # {
        #   session_id: {
        #         symbol: str,
        #         isCurrentPlayer: bool
        #         wantsToPlayAgain: bool
        #   }  
        # }
        
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
        
        if player_sid in self.players.keys():
            raise KeyError(f'The player of id: {player_sid} is already in the game')
        if len(self.players) > 2:
            raise ValueError("There can be at most 2 players in the room") # TODO: spectating
        
        self.players[player_sid] = {
            'symbol': 'O' if len(self.players) == 0 else 'X',
            'isCurrentPlayer':  len(self.players) == 0,
            'wantsToPlayAgain': False
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
            
    def update_board_state(self, index: int, player_sid: str) -> list:
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
        
        if player_sid not in self.players.keys():
            raise KeyError(f"There is no player with the {player_sid} in the game")
        if not index > -1 or not index < 9:
            raise IndexError(f"Index must be an integer in range 0-8")
        
        self.board_state[index] = self.players[player_sid]['symbol']
        self._change_turn()
        
        return self.board_state
    
    def _change_turn(self) -> None:
        for player_sid, player_state in self.players.items():
            self.players[player_sid]['isCurrentPlayer'] = not player_state['isCurrentPlayer']
    
    def clear_board(self) -> None:
        self.board_state = ['' for _ in range(9)]
        
    def check_for_game_end(self) -> Union[None, dict]:
        win_combos = (
            (0, 1, 2), (3, 4, 5),
            (6, 7, 8), (0, 4, 8),
            (2, 4, 6), (0, 3, 6),
            (1, 4, 7), (2, 5, 8)
            )
        
        for combo in win_combos:
            if self.board_state[combo[0]] == self.board_state[combo[1]] == self.board_state[combo[2]]:
                if self.board_state[combo[0]] != '':
                    self.game_ended = True
                    return {'winner': self.board_state[combo[0]]}
        else:
            if all([cell != '' for cell in self.board_state]):
                self.game_ended = True
                return {'winner': 'tie'}
    
    def player_wants_to_play_again(self, player_sid: str) -> None:
        if player_sid not in self.players.keys():
            raise KeyError(f"Player with the session id of \'{player_sid}\' is not in the room")
        
        self.players[player_sid]['wantsToPlayAgain'] = True
    
    def restart_game(self) -> bool:
        if not self.game_ended:
            raise PermissionError("The game is not finished!")
        
        if not all([player['wantsToPlayAgain'] for player in self.players.values()]):
            return False
        
        self.clear_board()
        
        for player, info in self.players.items():
            self.players[player]= {
                'symbol': 'O' if info['symbol'] == 'X' else 'X',
                'isCurrentPlayer': info['symbol'] == 'X',
                'wantsToPlayAgain': False
                }
    
        return True