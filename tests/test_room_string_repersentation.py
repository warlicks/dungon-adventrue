import pytest
from dungon.room import Room


@pytest.fixture
def r() -> Room:
    return Room(2, 2)


# Test Middle row of text that displays content.
def test_empyt_room_str(r):

    assert r._room_content_string() == "| |\n"
    assert str(r) == "*-*\n| |\n*-*"


def test_entrance_room_str(r):
    r.generate_room_content("entrance", True, 1.0)

    assert r._room_content_string() == "|i|\n"
    assert str(r) == "*-*\n|i|\n*-*"


def test_exit_room_str(r):
    r.generate_room_content("exit", True, 1.0)

    assert r._room_content_string() == "|O|\n"
    assert str(r) == "*-*\n|O|\n*-*"


def test_pit_room_str(r):

    r.generate_pit(probability=1.0)

    assert r._room_content_string() == "|X|\n"
    assert str(r) == "*-*\n|X|\n*-*"


def test_vision_potion(r):
    r.generate_room_content("vision potion", True, 1.0)

    assert r._room_content_string() == "|V|\n"
    assert str(r) == "*-*\n|V|\n*-*"


def test_health_potion(r):
    r.generate_healing_potion(probability=1.0)

    assert r._room_content_string() == "|H|\n"
    assert str(r) == "*-*\n|H|\n*-*"


def test_multiple(r):
    r.generate_healing_potion(probability=1.0)
    r.generate_pit(probability=1.0)

    assert r._room_content_string() == "|M|\n"
    assert str(r) == "*-*\n|M|\n*-*"


def test_pillar_string(r):
    r.generate_room_content("game_objective", "Abstraction", 1.0)

    assert r._room_content_string() == "|A|\n"
    assert str(r) == "*-*\n|A|\n*-*"
