from .room_events import RoomEvents
from .game_events import GameEvents
from .connection_events import ConnectionEvents

def initialize_all_handlers(socketio) -> None:
    RoomEvents(socketio)
    GameEvents(socketio)
    ConnectionEvents(socketio)

__all__ = [
    'RoomEvents',
    'GameEvents',
    'ConnectionEvents',
    'initialize_all_handlers'
]