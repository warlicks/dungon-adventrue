import random
from typing import Any


class Room:
    """Rooms in the Dungeon

    The Room class is intended to assist with the generation of the maze and to
    keep track of the room content during game play. he class does is not intended to
    handle any of the game playing logic. When a new room is created it is empty and the
    room is not connected to any other room in the maze.

    Attributes:
        x (int): The horizontal location of the room in the maze.
        y (int): The vertical location of the room in the maze.
        doors (dict): A dictionary indicating which of the four doors are connected
          to another room. If there is no room in a particular direction the value is False.
          If there is a room, the value is the Room instance.
        content (dict): The content in the room. The keys are the type of object in the
          room and value represents the value of the object. Only one of any object type
          can exist in a room.
    """

    def __init__(self, x: int, y: int) -> None:
        """Creates a new empty room.

        The Room class is intended to assist with the generation of the maze and to
        keep track of the room content during game play. When a new room is created it
        is empty and the room is not connected to any other room in the maze.

        Args:
            x (int): The horizontal location of the room in the maze.
            y (int): The vertical location of the room in the maze.
        """
        self.x = x
        self.y = y
        self.doors = {"North": False, "East": False, "South": False, "West": False}
        self.content = {}

    def generate_pit(
        self, min_damage: int = 1, max_damage: int = 20, probability: float = 0.1
    ):
        """Determines if a pit is in the room.

        A pit can cause 1 - 20 points of damage. The value of the pit damage is randomly
        generated. The presence of a pit is also randomly generated. The default
        probability of a pit being in the room is 0.1 or 10%

        Args:
            min_damage (int, optional): The minimum amount of damage caused by the pit.
              Defaults to 1.
            max_damage (int, optional): The maximum amount of damage caused by the pit.
              Defaults to 20.
            probability (float, optional): The probability of the pit being placed
              in the room. Defaults to 0.1.
        """
        pit_value = random.randint(min_damage, max_damage)
        self.generate_room_content("pit", pit_value, probability)

    def generate_healing_potion(
        self, min_healing: int = 5, max_healing: int = 15, probability: float = 0.1
    ):
        """Determines if a health potion is in the room.

        By default a health potion can ad 5-15 points of health. The value of health potion is
        randomly generated. The presence of the health potion in the room is also randomly
        generated.

        Args:
            min_healing (int, optional): The minimum amount of health a potion can restore. Defaults to 5.
            max_healing (int, optional): The maximum amount of health a potion can restore. Defaults to 15.
            probability (float, optional): The probability of the health potion being placed
              in the room. Defaults to 0.1.
        """

        potion_value = random.randint(min_healing, max_healing)
        self.generate_room_content("health potion", potion_value, probability)

    def generate_room_content(
        self, object_type: str, object_value: Any, probability: float = 0.1
    ) -> None:
        """Generates the content of the room.

        This function is intended to be very generic so that additional object types can
        be added to the game overtime. The placement of an object in the room is random
        and follows a binomial distribution. If you absolutely want the object to be
        found in the room set the probability to 1.0. If you want an even chance of the
        object being in the room set the value to 0.5

        Args:
            object_type (str): The type of object being added to the room.
            object_value (Any): The value of the object being added to the room.
            probability (float, optional): The probability of the object being placed
              in the room. Defaults to 0.1.

        Raises:
            ValueError: An invalid value for probability was provided when calling the API.
        """
        if probability < 0 or probability > 1.0:
            raise ValueError(
                "Probability must be a floating point value between 0.0 and 1.0"
            )
        if random.uniform(0, 1.0) >= (1 - probability):
            self.content[object_type] = object_value
