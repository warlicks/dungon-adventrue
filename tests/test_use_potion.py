import pytest
from io import StringIO
from dungon.dungeon_adventure import DungeonAdventure


@pytest.fixture
def test_dungeon():
    d = DungeonAdventure()
    d.adventurer.add_to_inventory("health potion", 10)
    d.adventurer.health_score = 80

    return d


def test_use_health(test_dungeon, monkeypatch):
    user_input = StringIO("10\n")
    monkeypatch.setattr("sys.stdin", user_input)

    test_dungeon.health_potion()

    assert test_dungeon.adventurer.health_score == 90
    assert not test_dungeon.adventurer.inventory["health potion"]


def test_no_health_to_use(test_dungeon, capsys):
    test_dungeon.adventurer.remove_from_inventory("health potion", 10)

    test_dungeon.health_potion()
    capture = capsys.readouterr()
    assert capture.out == """You don't have any health potion to use\n"""


""""
I tried to develop a test make sure this could handle bad input value for health
potion but ran into EOF errors. Manually checked it worked. See Terminal Output below.


\nYou have entered a new room located @ (1, 1)
\nYou found a Health Potion worth 13 health points in the Room. It has been added to your inventory.
You found Abstraction in the Room! It has been added to your inventory
What would you like to do now, Sean?
        Please Enter A Number from the Menu Below.
        1. Explore the Dungeon.
        2. Use A Health Potion.
        3. Use A Vision Potion.
        4. Check My Status.
        2
Which health potion would you like to use?13Please enter the value of the potion you would like to use: 10
Which health potion would you like to use?13Please enter the value of the potion you would like to use: E
Which health potion would you like to use?13Please enter the value of the potion you would like to use: 13
Your health has increased to 89
What would you like to do now, Sean?
"""
