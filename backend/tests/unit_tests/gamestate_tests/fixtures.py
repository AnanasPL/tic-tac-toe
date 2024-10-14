import pytest

from rooms import GameState


@pytest.fixture
def gs():
    gs = GameState()
    gs.add_player('XXX')
    gs.add_player('YYY')
    
    return gs