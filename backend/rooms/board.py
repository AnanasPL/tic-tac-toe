from typing import Union


class Board:
    def __init__(self) -> None:
        self._board_state = ['' for _ in range(9)]
    
    def clear(self) -> None:
        self._board_state = ['' for _ in range(9)]
        
    def update(self, index, symbol) -> None:
        if not index > -1 or not index < 9:
            raise IndexError(f"Index must be an integer in range 0-8")
        if self._board_state[index] != '':
            raise ValueError(f"The field with the index {index} is already taken")
        
        
        self._board_state[index] = symbol
        
    def get_state(self) -> list:
        return self._board_state
    
    def get_winner(self) -> Union[str, None]:
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
        