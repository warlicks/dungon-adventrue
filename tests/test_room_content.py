import pytest
from dungon.room import Room


def test_pit_creation():
    """Test the creation of the pit in the room.
    The test checks that we can change the min and max damage and the probability.
    In this case the probability guarantees we get a pit.
    """
    room = Room(0, 0)

    room.generate_pit(5, 10, 1.0)

    assert "pit" in room.content.keys()
    assert room.content["pit"] >= 5 and room.content["pit"] <= 10


def test_no_pit():
    """Test that not pit creation happens as expected.
    In this case we expect there to not be a pit key im the room content.
    """
    room = Room(0, 0)
    room.generate_pit(probability=0)

    assert len(room.content) == 0


def test_health_potion_creation():
    """Test the creation of the pit in the room.
    The test checks that we can change the min and max healing and the probability.
    In this case the probability guarantees we get a health potion.
    """
    room = Room(0, 0)

    room.generate_healing_potion(8, 12, 1.0)

    assert "health potion" in room.content.keys()
    assert room.content["health potion"] >= 8 and room.content["health potion"] <= 12


def test_no_health():
    """Test that no health potion creation happens as expected.
    In this case we expect there to not be a health potion key im the room content.
    """
    room = Room(0, 0)
    room.generate_healing_potion(probability=0)

    assert len(room.content) == 0


def test_general_content_creation():
    """Tests that we can generate any room content we want.
    Also allows us to demonstrate the creation of a vision potion.
    """
    room = Room(0, 0)
    room.generate_room_content("vision potion", True, 1.0)

    assert "vision potion" in room.content.keys()
    assert room.content["vision potion"] == True


def test_bad_probability():
    room = Room(0, 0)
    with pytest.raises(ValueError):
        room.generate_room_content("sword", 100, probability=2)


def test_bad_probability1():
    room = Room(0, 0)
    with pytest.raises(ValueError):
        room.generate_pit(probability=2)


def test_bad_probability2():
    room = Room(0, 0)
    with pytest.raises(ValueError):
        room.generate_healing_potion(probability=-0.5)
