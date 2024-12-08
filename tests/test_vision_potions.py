import pytest
from io import StringIO
from dungon.room import Room
from dungon.dungeon_adventure import DungeonAdventure
from random import random, seed, sample


@pytest.fixture
def test_dungeon_adv():
    """Create a dungeon adventure for testing the expected
    output from using Vision Potion"""
    d = DungeonAdventure()
    room1 = Room(1, 1)
    room2 = Room(2, 2)
    room3 = Room(3, 3)
    room4 = Room(4, 4)

    d.dungeon.rooms = [room1, room2, room3, room4]
    d.dungeon._map_height = 4
    d.dungeon._map_width = 4

    d.adventurer.add_to_inventory("vision potion", 1)

    return d


def test_room_vision(test_dungeon_adv):
    """Test expected output when using Vision Potion"""
    expected_room_vision = "               " \
                           "               " \
                           "               " \
                           "   *-*        " \
                           "   | |        " \
                           "   *-*        " \
                           "      *-*     " \
                           "      | |     " \
                           "      *-*     " \
                           "         *-*  " \
                           "         | |  " \
                           "         *-*  " \
                           "            *-*" \
                           "            | |"\
                           "            *-*"

    assert test_dungeon_adv.room_vision() == expected_room_vision




