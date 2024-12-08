import pytest
from io import StringIO
from dungon.room import Room
from dungon.dungeon_adventure import DungeonAdventure
from random import random, seed, sample


@pytest.fixture
def test_dungeonadv():
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


def test_room_vision(test_dungeonadv):
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

    assert test_dungeonadv.room_vision() == expected_room_vision


# def test_no_vision_potion(test_dungeonadv, monkeypatch, capsys):
#     test_dungeonadv.adventurer.inventory["vision potion"].pop(0) #remove vision potion
#     # "name" = test_dungeonadv.adventurer.name()
#
#     test_dungeonadv.chose_action()
#     user_input = StringIO("3\n")
#     captured = capsys.readouterr()
#     monkeypatch.setattr("sys.stdin", user_input)
#
#     assert captured.out == "Nice try! You can't use a Vision Potion unless it is in your inventory!\n"


