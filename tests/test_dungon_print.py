import pytest
from dungon.room import Room
from dungon.dungeon import Dungeon


@pytest.fixture
def dungeon() -> Dungeon:
    """Manually sets up Dungeon for testing"""

    room1 = Room(1, 1)
    room2 = Room(2, 2)
    room3 = Room(3, 3)
    room4 = Room(4, 4)

    d = Dungeon()
    d.rooms = [room1, room2, room3, room4]
    d._map_height = 4
    d._map_width = 4

    return d


def test_dungeon_print(dungeon):
    """Test the internal method for _map_whole_dungeon prints out as expected"""
    expected_print_room_map = [
        [
            "   ",
            "   ",
            "   ",
            "*-*\n| |\n*-*",
        ],
        ["   ", "   ", "*-*\n| |\n*-*", "   "],
        ["   ", "*-*\n| |\n*-*", "   ", "   "],
        ["*-*\n| |\n*-*", "   ", "   ", "   "],
    ]

    assert dungeon._map_whole_dungeon() == expected_print_room_map
