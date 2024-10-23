import pytest

from app import initialize_all_handlers, socketio
from errors import *

class TestEventHandler:
    def test_create_second_handler(self):
        with pytest.raises(HandlerAlreadyExistsError):
            initialize_all_handlers(socketio)