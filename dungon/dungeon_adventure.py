import random
from .adventurer import Adventurer
from .dungeon import Dungeon


class DungeonAdventure:
    def __init__(self) -> None:
        self.dungeon = Dungeon()
        self.current_room = None

    def start_game(self):
        # TODO: Print Welcome Message.

        # Set Up The Player
        player_name = input("Brave Explorer, what is your name?")
        self.adventurer = Adventurer(player_name)

        self.dungeon.generate_dungeon()
        print(f"Welcome to the Dungeon {self.adventurer.name}.")
        print(self.dungeon)

        # TODO: Randomly pick a room to start in.
        self.current_room = random.sample(self.dungeon.rooms, k=1)

    def chose_action(self):
        input_options = f"""What would you like to do now, {self.adventurer.name}?
        Please Enter A Number from the Menu Below. 
        1. Explore the Dungeon.
        2. Use A Health Potion.
        3. Use A Vision Potion.
        4. Check My Status. 
        """
        user_choice = input(input_options)
        while user_choice not in ["1", "2", "3", "4"]:
            user_choice = input(input_options)

        return int(user_choice)

    def move_rooms(self):
        move_options = f"""\nWhich direction would you like to move?\n\t1. North\n\t2. East\n\t3. South\n\t4. West\n"""
        move_keys = {"1": "North", "2": "East", "3": "South", "4": "West"}
        user_move_choice = input(move_options)

        while user_move_choice not in ["1", "2", "3", "4"]:
            user_move_choice = input(move_options)
        move_direction = move_keys[user_move_choice]
        if self.current_room.doors[move_direction] is not False:
            self.current_room = self.current_room.doors[move_direction]
        else:
            print(f"There is no room to the {move_keys[user_move_choice]}")

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