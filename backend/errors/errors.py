class PlayerNotFoundError(Exception):
    """Raised when there is no player with the given session id"""
    
class FieldAlreadyTakenError(Exception):
    """Raised when the field was already taken by another player"""
    
class TurnError(Exception):
    """Raised when it's not the turn of the player"""

class RoomAlreadyFullError(Exception):
    """Raised when the room is already full"""