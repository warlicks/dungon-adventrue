import pytest
from dungon import dungeon
from dungon.dungeon import Dungeon
from dungon.room import Room


def test_new_room_north():
    """Test that room1 North door connects to room 2 south door."""
    room1 = Room(3, 5)
    room2 = Room(3, 20)

    dungon = Dungeon()

    dungon._connect_rooms(room2, room1)

    assert room1.doors["North"] == room2
    assert room2.doors["South"] == room1


def test_new_room_south():
    """Test that rooms are correctly positioned when new room is south of previous room"""
    room1 = Room(20, 16)
    room2 = Room(20, 13)

    dungeon = Dungeon()

    dungeon._connect_rooms(room2, room1)

    assert room1.doors["South"] == room2
    assert room2.doors["North"] == room1


def test_new_room_east():
    """Test That rooms are connected correctly when new room is east of previous room."""
    room1 = Room(5, 6)
    room2 = Room(8, 6)

    dungeon = Dungeon()
    dungeon._connect_rooms(room2, room1)

    assert room1.doors["East"] == room2
    assert room2.doors["West"] == room1


def test_new_room_west():
    """Test that rooms are connected correctly when new room is west of previous room."""
    room1 = Room(12, 9)
    room2 = Room(-1, 9)

    dungeon = Dungeon()
    dungeon._connect_rooms(room2, room1)

    assert room1.doors["West"] == room2
    assert room2.doors["East"] == room1


def test_new_room_ne():
    """Test that the rooms are connected correctly when new room is NE of previous room

    Since the "tunnel path" (horizontal first or vertical first) is randomly chosen this
    test case checks for either correct solution.
    """

    room1 = Room(3, 5)
    room2 = Room(6, 7)

    dungeon = Dungeon()
    dungeon._connect_rooms(room2, room1)

    assert ((room1.doors["East"] == room2) and (room2.doors["South"] == room1)) or (
        (room1.doors["North"] == room2) and (room2.doors["West"] == room1)
    )


def test_new_room_se():
    """Test that the rooms are connected correctly when new room is SE of previous room

    Since the "tunnel path" (horizontal first or vertical first) is randomly chosen this
    test case checks for either correct solution.
    """
    room1 = Room(6, 7)
    room2 = Room(9, 3)

    dungeon = Dungeon()
    dungeon._connect_rooms(room2, room1)

    assert ((room1.doors["East"] == room2) and (room2.doors["North"] == room1)) or (
        (room1.doors["South"] == room2) and room2.doors["West"] == room1
    )


def test_new_room_nw():

    room2 = Room(6, 7)  # New Room
    room1 = Room(9, 3)  # Previous room

    dungeon = Dungeon()
    dungeon._connect_rooms(room2, room1)

    assert ((room1.doors["West"] == room2) and (room2.doors["South"] == room1)) or (
        (room1.doors["North"] == room2) and room2.doors["East"] == room1
    )


def test_new_room_sw():
    room1 = Room(9, 3)
    room2 = Room(4, 1)

    dungeon = Dungeon()
    dungeon._connect_rooms(room2, room1)

    assert ((room1.doors["West"] == room2) and (room2.doors["North"] == room1)) or (
        (room1.doors["South"] == room2) and room2.doors["East"] == room1
    )
