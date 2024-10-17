import pytest

from rooms import *
from errors import *

@pytest.fixture
def rooms():
    r = Rooms()
    room = Room()
    room2 = Room()
    
    r.add_rooms(room, room2)
    
    return r, room, room2