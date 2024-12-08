import pytest
from dungon.dungeon_adventure import DungeonAdventure
from dungon.dungeon import Dungeon
from dungon.room import Room


@pytest.fixture
def winning_dungeon() -> DungeonAdventure:
    """Set up dungeon and adventure in situation to win."""
    room = Room(4, 4)
    room.generate_room_content("exit", True, 1.0)

    d = DungeonAdventure()
    d.adventurer.add_to_inventory("pillar", "Abstraction")
    d.adventurer.add_to_inventory("pillar", "Encapsulation")
    d.adventurer.add_to_inventory("pillar", "Inheritance")
    d.adventurer.add_to_inventory("pillar", "Polymorphism")

    d.dungeon.rooms.append(room)
    d.current_room = room

    return d


@pytest.fixture
def losing_dungeon() -> DungeonAdventure:
    """Set up dungeon and adventure in situation to win."""
    room = Room(4, 4)
    room.generate_room_content("exit", True, 1.0)

    d = DungeonAdventure()
    d.adventurer.add_to_inventory("pillar", "Abstraction")
    d.adventurer.add_to_inventory("pillar", "Encapsulation")
    d.adventurer.add_to_inventory("pillar", "Inheritance")

    d.dungeon.rooms.append(room)
    d.current_room = room

    return d


def test_winning(winning_dungeon, capsys):

    winning_dungeon.maze_exit_outcome()
    capture = capsys.readouterr()
    assert capture.out.startswith("You Win!\n")
    assert winning_dungeon.continue_game is False


def test_losing(losing_dungeon, capsys):

    losing_dungeon.maze_exit_outcome()
    capture = capsys.readouterr()
    assert capture.out.startswith(
        "\nYou'll be stuck debugging poorly documented issues until the end of time"
    )
    assert capture.out.endswith("Polymorphism\n")
    assert losing_dungeon.continue_game is False


def test_losing_health(winning_dungeon, capsys):
    exp_msg = "You Died Dungeon of Perpetual Code Bugs!\n The Dungeon is a dangerous place. Play again; if you are brave enough!\n"
    winning_dungeon.adventurer.health_score = 0

    winning_dungeon.check_player_health()
    capture = capsys.readouterr()
    assert capture.out == exp_msg
    assert winning_dungeon.continue_game is False
