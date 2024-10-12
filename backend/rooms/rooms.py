from string import ascii_letters, digits
from random import choice
from typing import Union

from .gamestate import GameState
from .player import Player

class Room:
    """A room for Tic-Tac-Toe game with Flask SocketIO
    
    Attributes:
        code (int): 
            Randomly generated code of the length given at the initialization
            (6 by default), made only by lower- and uppercase letters and digits
        game_state (GameState): Current game state
    """
    
    def __init__(self, code_length: int = 6) -> None:
        """
        Args:
            code_length (int, optional): The length of a randomly generated code. `6` by default
        """
        self.code = self.generate_room_code(code_length)
        self.game_state = GameState()

    @staticmethod
    def generate_room_code(length: int = 6) -> str:
        """Generates a room code of the given length

        Args:
            length (int, optional): The length of the generated code. `6` by default

        Returns:
            str: 
                The code of the given length, containing only 
                lower- and uppercase letters and digits
        """
        allowed_characters = ascii_letters + digits
        room_code = ""
        
        for _ in range(length):
            room_code += choice(allowed_characters)
            
        return room_code
    
    def add_player(self, session_id: str) -> Player:
        """Adds player to the room

        Args:
            session_id (str): The session id of the player

        Returns:
            Player: The player object of the added player
        """
        return self.game_state.add_player(session_id)
        
    def remove_player(self, session_id: str) -> None:
        """Removes player from the room
        
        Args:
            session_id (str): The session id of the player
        """
        
        self.game_state.remove_player(session_id)
            
    def get_players_session_ids(self) -> tuple[str]:
        """Returns a tuple with all the session ids of the players in the room"""
        return self.game_state.get_players_session_ids()
    
    def get_size(self) -> int:
        """Returns how many players that are in the room"""
        return len(self.game_state.players)


class Rooms:
    """Managing Flask SocketIO rooms"""
    
    def __init__(self) -> None:
        self._rooms: list[Room] = []
    
    def add_rooms(self, *args: Room) -> None:
        """
        Adds room(s) to the rooms list
        
        Args:
            *args (Room): A sequence of Room objects that will be added.
        """
        
        [self._add_room(room) for room in args]
        
    def _add_room(self, room: Room) -> None:
        """Adds a single room to the rooms list

        Args:
            room (Room): Room class instance to add
        """
        self._rooms.append(room)
    
    def get_all_codes(self) -> tuple[str]:
        """Returns a tuple with all of the codes of every room in the rooms list"""
        
        return (room.code for room in self._rooms)
    
    def get_all_players_session_ids(self) -> tuple[str]:
        """Returns a tuple with all the session ids of the users in the rooms"""
        
        return (sid for room in self._rooms for sid in room.get_players_session_ids())
    
    def remove_empty_rooms(self) -> None:
        """Removes all rooms with no players from the rooms list"""
        self._rooms = tuple(filter(lambda room: room.get_size() != 0, self._rooms))

    def get_first_available_room(self) -> Union[Room, None]:
        """Returns first non-full room, or None if there is no such."""
        
        if self.all_rooms_full():
            return None
        
        return list(filter(lambda room: room.get_size() == 1, self._rooms))[0]

    def all_rooms_full(self) -> bool:
        """Returns `True` if all rooms are full, `False` otherwise."""
        
        return all(room.get_size() == 2 for room in self._rooms)
    
    def get_player_room(self, session_id: str) -> Room:
        """Returns the room that the player is currently in
        
        Args:
            session_id (str): The session id of the player
            
        Returns:
            Room: The room that the player is currently connected to
            
        Raises:
            KeyError: If the player is not in any room
        """
        
        if not session_id in self.get_all_players_session_ids():
            raise KeyError(f"The player with given session id {session_id} is not in any room")
        
        return list(filter(lambda room: session_id in room.get_players_session_ids(), self._rooms))[0]
    
    def get_room_by_code(self, code: int) -> Union[Room, None]:
        """Returns the Room that has the given code. `None` if there is no such.

        Args:
            code (int): code of the room
        """
        
        if code not in self.get_all_codes():
            return None
        
        return list(filter(lambda room: room.code == code, self._rooms))[0]

    def get_rooms_info(self) -> tuple[tuple[str, int]]:
        """Returns basic information about every room

        Returns:
            tuple[tuple[str, int]]: 
                A tuple of 2-element tuples, made of string,
                representing a room code and its size 
        """
        return ((room.code, room.get_size()) for room in self._rooms)