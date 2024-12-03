from typing import Any, Dict, Union
import random


class Adventurer:
    """Manages the player avatar as the game proceeds.

    The Adventurer Class manages the players avatar throughout the game. The main game
    play logic interacts with the avatar rather than keeping track of avatar directly.
    The class keeps track of the players health and their inventory. It also contains
    methods for working with the players health and inventory.

    Attributes:
        Inventory(dict): Contains the avatars inventory. The inventory is set up as
          dictionary where the keys indicate the item types. Each item of that
          type is stored in a list. For example, if a player has two health potions it's
          represented as {"heal potion": [10, 5]}
    """

    def __init__(self, name: Union[str, None]) -> None:
        """Creates an instance of an adventurer to explore the dungeon.

        Args:
            name (str): The name of the adventurer.
        """
        self._name = name
        self.health_score = random.randint(75, 100)

        # Dictionary makes if flexible to add other objects to the game play.
        # Currently set up for the 3 initial items in the game.
        self.inventory = {"health potion": [], "vision potion": [], "pillar": []}

    @property
    def name(self) -> str:
        """The name of the players avatar"""
        return self._name

    @property
    def health_score(self) -> int:
        """The number of health points for the avatar

        The avatars health score is an integer value between 0 and 100. If adjustments
        to the avatars health score goes would make it greater than 100 the score
        is set to 100. Like wise if the adjustments set the score blow zero it goes to
        zero.

        Returns:
            int: integer
        """
        return self._health_score

    @health_score.setter
    def health_score(self, value):
        # handle cases were values go above 100 or below zero.
        if value > 100:
            self._health_score = 100
        elif value < 0:
            self._health_score = 0
        else:
            self._health_score = value

    def increase_health(self, amount: int) -> None:
        """Increase the avatars health score by the set amount.

        See health_score for more details.

        Args:
            amount (int): The amount to increase the avatars health score.
        """

        self.health_score += amount

    def decrease_health(self, amount: int) -> None:
        """Decreases the avatars health score by the set amount.

        Args:
            amount (int): The amount to decrease the avatars health score.
        """
        self.health_score -= amount

    def add_to_inventory(self, object_type: str, object_value: Any):
        """Adds an item to the avatars inventory.

        Args:
            object_type (str): They type of object being added to the inventory
            object_value (Any): The value of the time being added to inventory.
        """

        if object_type in self.inventory.keys():
            self.inventory[object_type].append(object_value)
        else:
            self.inventory[object_type] = list()
            self.inventory[object_type].append(object_value)

    def remove_from_inventory(self, object_type: str, object_value: Any):
        # Then len check handles the case for health, vision potion or pillar are empty.
        if (
            object_type not in self.inventory.keys()
            or len(self.inventory[object_type]) == 0
        ):
            print(f"No {object_type} is in inventory.")
        elif object_value not in self.inventory[object_type]:
            print(f"No {object_type} with {object_value} is in inventory.")
        else:
            self.inventory[object_type].remove(object_value)

    def player_status(self):
        """Print current status of the avatar.

        Status reports the avatar's name, the health score and the items inventory.

        """
        print(self.__str__())

    def __str__(self) -> str:
        full_inventory = []
        for key in self.inventory.keys():
            full_inventory.append(
                f"{len(self.inventory[key])} {key} with value(s): {self.inventory[key]}"
            )

        # TODO: Use the suggestion in Google's style guide to make this pretty.
        joined_message = "\n\t".join(full_inventory)
        status_msg = f"""
        {self.name} has {self.health_score} health points.
        {self.name} has the following items in inventory:
        {joined_message}
        """
        return status_msg
