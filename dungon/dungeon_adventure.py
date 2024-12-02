from .adventurer import Adventurer
from .dungeon import Dungeon


class DungonAdventure:
    def __init__(self) -> None:
        self.dungeon = Dungeon()

    def start_game(self):
        # TODO: Print Welcome Message.

        # Set Up The Player
        player_name = input("Brave Explorer, what is your name?")
        self.adventurer = Adventurer(player_name)

        # TODO: Create The Dungeon
        self.dungeon.generate_dungeon()
        # TODO: Randomly pick a room
        current_room = self.dungeon.rooms[0]

    def pick_up_health_potion(self, potion_value: int):
        self.adventurer.add_to_inventory("health potion", potion_value)
        # TODO: Fix this to make it talk to the player.

        print(
            f"Added a health potion with {potion_value} to {self.adventurer.name}'s inventory"
        )

    def pick_up_vision_potion(self, potion_value: int = 1):
        self.adventurer.add_to_inventory("vision potion", potion_value)
        # TODO: Fix this to make it talk to the player.
        print(f"Added a Vision Potion to {self.adventurer.name}'s inventory")

    def pick_up_pillar(self, pillar_name: str):
        self.adventurer.add_to_inventory("pillar", pillar_name)
        print(
            f"You found {pillar_name} in the Room! It has been added to your inventory"
        )
        # TODO: Print message about the pillars you still need to find.

    def _check_player_health(self) -> bool:
        """Internal checks to see if the avatar still has health, used to determine
        if the game continues.
        """

        if self.adventurer.health_score == 0:
            return False
        else:
            return True
