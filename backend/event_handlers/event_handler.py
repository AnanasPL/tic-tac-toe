from abc import ABC, abstractmethod


class EventHandler(ABC):
    @abstractmethod
    def register_events(self):
        pass