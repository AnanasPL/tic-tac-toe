from string import ascii_letters, digits
from random import choice
from typing import Any, Union

from .gamestate import GameState

class Room:
    def __init__(self, code_length: int = 6) -> None:
        self.code = self.generate_room_code(code_length)
        self.game_state = GameState()

    @staticmethod
    def generate_room_code(length: int = 6) -> str:
        allowed_characters = ascii_letters + digits
        room_code = ""
        
        for _ in range(length):
            room_code += choice(allowed_characters)
            
        return room_code
    
    # TODO: names
    def add_player(self, session_id: str) -> dict:
        return self.game_state.add_player(session_id)
        
    def remove_player(self, session_id: str) -> dict:        
        self.game_state.remove_player(session_id)
            
    def get_players_session_ids(self) -> list[str]:
        return self.game_state.players.keys()
    
    def get_size(self) -> int:
        return len(self.game_state.players)


class Rooms:
    """
    Room management
    
    Attributes:
        _rooms (list[Room]): a list of all rooms.
    """
    
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
        self._rooms.append(room)
    
    def get_all_codes(self) -> list[str]:
        """Returns the list of codes of every room in the room list."""
        
        return [room.code for room in self._rooms]
    
    def get_all_players_session_ids(self) -> list[str]:
        """Returns a list of all session ids of the users in the rooms."""
        
        return [sid for room in self._rooms for sid in room.get_players_session_ids()]
    
    def remove_empty_rooms(self) -> None:
        """Removes all empty rooms from the rooms list."""
        self._rooms = list(filter(lambda room: room.get_size() != 0, self._rooms))

    def get_first_available_room(self) -> Union[Room, None]:
        """Returns first available room, or None if there is no such."""
        
        if self.all_rooms_full():
            return None
        
        return list(filter(lambda room: room.get_size() == 1, self._rooms))[0]

    def all_rooms_full(self) -> bool:
        """Returns True if all rooms are full, false otherwise."""
        
        return all(room.get_size() == 2 for room in self._rooms)
    
    def get_player_room(self, session_id: str) -> Room:
        """
        Returns the room that the player is currently connected to
        
        Args:
            session_id (str): session id of the player
            
        Returns:
            Room: The room that the player is currently connected to
            
        Raises:
            KeyError: If the player is not found in any room
        """
        
        if not session_id in self.get_all_players_session_ids():
            raise KeyError(f"The player with given session id {session_id} is not in any room")
        
        return list(filter(lambda room: session_id in room.get_players_session_ids(), self._rooms))[0]
    
    def get_room_by_code(self, code: int) -> Union[Room, None]:
        """
        Returns the Room that has the given code. None if there is no such.

        Args:
            code (int): code of the room
        """
        
        if code not in self.get_all_codes():
            return None
        
        return list(filter(lambda room: room.code == code, self._rooms))[0]

    def get_rooms_info(self):        
        return [(room.code, room.get_size()) for room in self._rooms]