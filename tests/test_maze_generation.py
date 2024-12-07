import pytest
from dungon.dungeon import Dungeon


@pytest.fixture
def dungeon() -> Dungeon:
    """Create a dungeon with 6 rooms to test generation

    Six rooms is the minimum needed to test that we have an entrance, an exit and
    all four pillars of object oriented programming. It is also a reasonable size for
    making sure all the rooms are connected.

    Since pits, health potions and vision potions are randomly created, I'm not going to
    test their presence.
    """
    d = Dungeon(max_rooms=6)
    d.generate_dungeon()

    return d


def test_small_maze_generation(dungeon):
    """Check that we get the correct number of rooms."""

    assert len(dungeon.rooms) == 6


def test_entrance_present(dungeon):
    "Check That we Have 1 entrance in the maze."
    assert "entrance" in dungeon.object_counts.keys()
    assert dungeon.object_counts["entrance"] == 1
    # Make sure entrance was assigned to the first room.
    assert dungeon.rooms[0].content["entrance"]


def test_exit_present(dungeon):
    "Check That we Have 1 Exit in the maze."
    assert "exit" in dungeon.object_counts.keys()
    assert dungeon.object_counts["exit"] == 1
    # Make sure entrance was assigned to the first room.
    assert dungeon.rooms[-1].content["exit"]


def test_that_game_objectives_placed(dungeon):
    "Check that all 4 objectives have been placed."
    assert "game_objective" in dungeon.object_counts.keys()
    assert dungeon.object_counts["game_objective"] == 4


def test_four_unique_objectives(dungeon):
    pillars = []
    for r in dungeon.rooms:
        if "game_objective" in r.content.keys():
            pillars.append(r.content["game_objective"])

    a = [
        x in pillars
        for x in ["Abstraction", "Encapsulation", "Inheritance", "Polymorphism"]
    ]
    assert all(a)


# Here down we test basic navigation by making sure rooms are connected as expected.
def test_navigation_room0_to_room1(dungeon):

    assert dungeon.rooms[1] in dungeon.rooms[0].doors.values()
    assert dungeon.rooms[0] in dungeon.rooms[1].doors.values()


def test_room1_to_room2(dungeon):
    assert dungeon.rooms[2] in dungeon.rooms[1].doors.values()
    assert dungeon.rooms[1] in dungeon.rooms[2].doors.values()


def test_room2_to_room3(dungeon):
    assert dungeon.rooms[3] in dungeon.rooms[2].doors.values()
    assert dungeon.rooms[2] in dungeon.rooms[3].doors.values()


def test_room3_to_room4(dungeon):
    assert dungeon.rooms[4] in dungeon.rooms[3].doors.values()
    assert dungeon.rooms[3] in dungeon.rooms[4].doors.values()


def test_room4_to_room5(dungeon):
    assert dungeon.rooms[5] in dungeon.rooms[4].doors.values()
    assert dungeon.rooms[4] in dungeon.rooms[5].doors.values()


def test_error_too_few_rooms():
    """Test that we get an error if we can't place all the game objectives."""
    dungeon = Dungeon(max_rooms=4)

    with pytest.raises(ValueError):
        dungeon.generate_dungeon()


def test_larger_room_size():
    """Test that we can create as many rooms as we want"""
    dungeon = Dungeon(max_rooms=50)
    dungeon.generate_dungeon()

    assert len(dungeon.rooms) == 50
