import pytest
from dungon.room import Room
from dungon.dungeon_adventure import DungeonAdventure


def test_empty_room_check(capsys):
    """Test that checking the room content returns a message when room is empty"""
    d = DungeonAdventure()
    room0 = Room(2, 2)
    d.dungeon.rooms.append(room0)
    d.current_room = d.dungeon.rooms[0]

    d.check_room_content()
    capture = capsys.readouterr()

    assert capture.out == """\\nThe current room is empty\n"""


def test_health_potion_in_room(capsys):
    """Test that a health potion is picked up when in the room
    Tests when a potion is in the room it is:
      1. added to the avatar's inventory
      2. removed from the room's content.
    """
    d = DungeonAdventure()
    room0 = Room(2, 2)
    room0.content["health potion"] = 10
    d.dungeon.rooms.append(room0)
    d.current_room = d.dungeon.rooms[0]

    d.check_room_content()
    capture = capsys.readouterr()

    assert (
        capture.out
        == "\\nYou found a Health Potion worth 10 health points in the Room. It has been added to your inventory.\n"
    )
    assert d.adventurer.inventory["health potion"][0] == 10
    assert "health potion" not in d.current_room.content.keys()


def test_vision_potion_in_room(capsys):
    """Test that a vision potion is picked up when in the room
    Tests when a potion is in the room it is:
      1. added to the avatar's inventory
      2. removed from the room's content.
    """
    d = DungeonAdventure()
    room0 = Room(2, 2)
    room0.content["vision potion"] = True
    d.dungeon.rooms.append(room0)
    d.current_room = d.dungeon.rooms[0]

    d.check_room_content()
    capture = capsys.readouterr()

    assert (
        capture.out
        == "You found a Vision Potion in the room. It has been added to your inventory.\n"
    )
    assert d.adventurer.inventory["vision potion"][0]
    assert "vision potion" not in d.current_room.content.keys()


def test_game_pillar_in_room(capsys):
    """Test that a pillar is found and added to the player inventory.
    After adding to inventory it should be removed from the room content.
    """
    d = DungeonAdventure()
    room0 = Room(2, 2)
    room0.content["game_objective"] = "Inheritance"
    d.dungeon.rooms.append(room0)
    d.current_room = d.dungeon.rooms[0]

    d.check_room_content()
    capture = capsys.readouterr()

    assert (
        capture.out
        == "You found Inheritance in the Room! It has been added to your inventory\n"
    )
    assert d.adventurer.inventory["pillar"][0] == "Inheritance"
    assert "game_objective" not in d.current_room.content.keys()


def test_multiple_items_in_room():
    """That multiple items in the room are picked up and added to inventory."""
    d = DungeonAdventure()
    room0 = Room(2, 2)
    room0.content["game_objective"] = "Inheritance"
    room0.content["vision potion"] = True
    room0.content["health potion"] = 10
    d.dungeon.rooms.append(room0)
    d.current_room = d.dungeon.rooms[0]

    d.check_room_content()
    assert d.adventurer.inventory["health potion"][0] == 10
    assert d.adventurer.inventory["vision potion"][0]
    assert d.adventurer.inventory["pillar"][0] == "Inheritance"
    assert len(d.current_room.content.keys()) == 0


def test_falling_in_pit(capsys):
    """That multiple items in the room are picked up and added to inventory."""
    d = DungeonAdventure()
    room0 = Room(2, 2)
    room0.content["pit"] = 20
    d.dungeon.rooms.append(room0)
    d.current_room = d.dungeon.rooms[0]

    starting_health = d.adventurer.health_score

    d.check_room_content()
    capture = capsys.readouterr()
    assert capture.out.startswith("You fell in a pit!")
    assert d.adventurer.health_score == (starting_health - 20)
    # We don't remove the pit from the room. They can keep falling in it!
    assert "pit" in d.current_room.content.keys()
