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
