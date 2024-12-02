import pytest
from dungon.adventurer import Adventurer


@pytest.fixture
def dungeon_explorer() -> Adventurer:
    a = Adventurer("Player 1")

    return a


def test_player_name(dungeon_explorer):
    """Test that the name get's set correctly at instance creation"""
    assert dungeon_explorer.name == "Player 1"

def test_add_health(dungeon_explorer):
    """Test that health is correctly update.
    Also checks that the starting health is between 75 and 100. 
    
    Since starting health is randomly set the test is designed to handle case where the 
    starting value is above 90 so the expected value caps out at 100 as it should.
    """
    starting_health = dungeon_explorer.health_score
    
    # IF our starting health would go over 100 we need to set our expect3ed value to 
    # 100. Otherwise we just do math. 
    if starting_health >= 90:
        expected_value = 100
    else:
        expected_value = starting_health + 10
    dungeon_explorer.increase_health(10)

    assert starting_health >= 75 and starting_health <= 100
    assert dungeon_explorer.health_score == expected_value

def test_subtract_health(dungeon_explorer):
    """Test that health is correctly subtracted"""
    starting_health = dungeon_explorer.health_score
    dungeon_explorer.decrease_health(20)
    assert dungeon_explorer.health_score == (starting_health - 20)

def test_subtract_health_below_zero(dungeon_explorer):
    """Test if value goes below zero it returns zero
    I use an extreme value here to make sure it will be go below zero. 
    """
    dungeon_explorer.decrease_health(200)

    assert dungeon_explorer.health_score == 0

def test_known_keys(dungeon_explorer):
    """Test that we can add health, vision and game objectives to the inventory
    Also tests that we can use any data type to represent the inventory item. 
    """
    original_keys = dungeon_explorer.inventory.keys()
    dungeon_explorer.add_to_inventory("health potion", 10)
    dungeon_explorer.add_to_inventory("vision potion", True)
    dungeon_explorer.add_to_inventory("pillar", "E")
    
    assert dungeon_explorer.inventory.keys() == original_keys
    assert len(dungeon_explorer.inventory["health potion"]) == 1
    assert len(dungeon_explorer.inventory["vision potion"]) == 1
    assert len(dungeon_explorer.inventory["pillar"]) == 1

def test_new_inventory_type(dungeon_explorer):
    """Test we can easily add new object types to the inventory."""
    dungeon_explorer.add_to_inventory("sword", 100)
    assert "sword" in dungeon_explorer.inventory.keys()
    assert len(dungeon_explorer.inventory.keys()) == 4

def test_no_wand_inventory(dungeon_explorer, capsys):
    """Test the the correct message is printed when you try to remove an 
    item is not in inventory. 
    """
    dungeon_explorer.remove_from_inventory("magic wand", 10)
    capture = capsys.readouterr()


    assert capture.out == "No magic wand is in inventory.\n"

def test_wrong_health_potion(dungeon_explorer, capsys):
    """Test that the function handles when an item type is present, but an item of that
    value isn't present."""
    dungeon_explorer.add_to_inventory("health potion", 10)
    dungeon_explorer.remove_from_inventory("health potion", 100)
    capture = capsys.readouterr()

    assert capture.out == "No health potion with 100 is in inventory.\n"


def test_remove_proper_sword(dungeon_explorer):
    """Test that an item in inventory is correctly removed."""
    dungeon_explorer.add_to_inventory('sword', 100)
    dungeon_explorer.remove_from_inventory("sword", 100)

    assert len(dungeon_explorer.inventory["sword"]) == 0