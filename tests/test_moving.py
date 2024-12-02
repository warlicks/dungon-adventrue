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
    assert capture.out.endswith("\nThere is no room to the North\n")
