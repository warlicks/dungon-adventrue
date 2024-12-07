import pytest
from io import StringIO
from dungon.dungeon_adventure import DungeonAdventure
from dungon.room import Room


@pytest.fixture
def dungeon():
    d = DungeonAdventure()

    # Manually Set Up Rooms
    room0 = Room(2, 5)
    room1 = Room(3, 5)

    room0.doors["East"] = room1
    room1.doors["West"] = room0

    d.dungeon.rooms = [room0, room1]
    d.current_room = room0
    return d


def test_successful_move(dungeon, monkeypatch):
    """"""
    user_input = StringIO("2\n")
    monkeypatch.setattr("sys.stdin", user_input)

    dungeon.move_rooms()

    assert dungeon.current_room == dungeon.dungeon.rooms[1]


def test_unsuccessful_move(dungeon, monkeypatch, capsys):
    user_input = StringIO("1\n")
    monkeypatch.setattr("sys.stdin", user_input)
    dungeon.move_rooms()
    capture = capsys.readouterr()

    # The print capture catches the print from when we capture user input and the
    # response when we can't navigate to the north. Therefore we use the endswith() to
    # just check the end of the print statement.
    assert capture.out.endswith("The door to the North is blocked.\n")


@pytest.fixture
def three_room_dungeon():
    d = DungeonAdventure()

    # Manually Set Up Rooms
    room0 = Room(2, 5)
    room1 = Room(3, 5)
    room2 = Room(4, 2)

    room0.doors["East"] = room1
    room1.doors["West"] = room0
    room1.doors["East"] = room2
    room2.doors["North"] = room1

    d.dungeon.rooms = [room0, room1, room2]
    d.current_room = room1
    return d


def test_movement_with_multiple_con(three_room_dungeon, monkeypatch):
    user_input = StringIO("4\n")
    monkeypatch.setattr("sys.stdin", user_input)
    three_room_dungeon.move_rooms()

    assert three_room_dungeon.current_room == three_room_dungeon.dungeon.rooms[0]

    user_input = StringIO("2\n")
    monkeypatch.setattr("sys.stdin", user_input)
    three_room_dungeon.move_rooms()

    assert three_room_dungeon.current_room == three_room_dungeon.dungeon.rooms[1]

    user_input = StringIO("2\n")
    monkeypatch.setattr("sys.stdin", user_input)
    three_room_dungeon.move_rooms()

    assert three_room_dungeon.current_room == three_room_dungeon.dungeon.rooms[2]
