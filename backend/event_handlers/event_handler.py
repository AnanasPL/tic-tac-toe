from abc import ABC, ABCMeta, abstractmethod
from errors import HandlerAlreadyExistsError


class EventHandlerMeta(ABCMeta):
    _handlers = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._handlers:
            instance = super().__call__(*args, **kwargs)
            cls._handlers[cls] = instance
            return instance
        
        raise HandlerAlreadyExistsError(f"{cls.__name__} already exists")

class EventHandler(ABC, metaclass=EventHandlerMeta):
    def __init__(self, socketio):
        self.socketio = socketio
        self.register_events()

    @abstractmethod
    def register_events(self):
        pass
    