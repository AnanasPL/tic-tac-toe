from typing import Union
from errors import FieldAlreadyTakenError


class Board:
    """Board of a Tic-Tac-Toe game"""
    
    def __init__(self) -> None:
        self._board_state: list[str] = ['' for _ in range(9)]
    
    def clear(self) -> None:
        """Resets the board state to the starting one (an array containing 9 empty strings)"""
        self._board_state = ['' for _ in range(9)]

    def update(self, index: int, symbol: str) -> None:
        """Updates the current board state

        Args:
            index (int): 
                Index of the field to change \n
                0 | 1 | 2\n
                ---------\n
                3 | 4 | 5\n
                ---------\n
                6 | 7 | 8
                
            symbol (str): The symbol to change the field into

        Raises:
            IndexError: If the index is not in the range 0-8
            FieldAlreadyTakenError: If the field is already taken
        """
        if not index > -1 or not index < 9:
            raise IndexError(f"Index must be an integer in range 0-8")
        if self._board_state[index] != '':
            raise FieldAlreadyTakenError(f"The field with the index {index} is already taken")
        
        self._board_state[index] = symbol
        
    def get_state(self) -> list:
        """Returns the current board state"""
        return self._board_state
    
    def get_winner(self) -> Union[str, None]:
        """Returns the winner of the game

        Returns:
            str:
                `O` or `X` if there is a winner, and `tie` if the game has ended and
                neither of the players won
                
            None: 
                If there is no winner and the game is still in progress
        """
        win_combos = (
            (0, 1, 2), (3, 4, 5),
            (6, 7, 8), (0, 4, 8),
            (2, 4, 6), (0, 3, 6),
            (1, 4, 7), (2, 5, 8)
            )
        
        for (i, j, k) in win_combos:
            if self._board_state[i] == '':
                continue
            
            if self._board_state[i] == self._board_state[j] == self._board_state[k]:
                return self._board_state[i]
            
        if all(cell != '' for cell in self._board_state):
            return 'tie'
        