from string import ascii_letters, digits

from rooms import Room
import pytest


class TestRoomCodeGeneration:
    length_range_1_30 = pytest.mark.parametrize('length', [i for i in range(1, 30)])
    
    @length_range_1_30
    def test_code_length(self, length):
        code = Room.generate_room_code(length)
        
        assert len(code) == length
        
    @pytest.mark.parametrize('length', [i for i in range(-30, 0)])
    def test_code_length_not_positive(self, length):
        with pytest.raises(ValueError):
            Room.generate_room_code(length)
        
    @length_range_1_30
    def test_code_contains_only_eligible_characters(self, length):
        eligible_characters = ascii_letters + digits
        code = Room.generate_room_code(length)
        
        assert all(char in eligible_characters for char in code)
