import random
from .adventurer import Adventurer
from .dungeon import Dungeon


class DungeonAdventure:
    def __init__(self) -> None:
        self.dungeon = Dungeon()
        self.adventurer = Adventurer(None)
        self.current_room = None

    def start_game(self):
        # TODO: Print Welcome Message.

        # Set Up The Player
        player_name = input("Brave Explorer, what is your name?\n\tEnter Your Name: ")
        self.adventurer.name = player_name

        self.dungeon.generate_dungeon()
        print(f"Welcome to the Dungeon {self.adventurer.name}.\n")
        print("As you start your exploration your status is:\n")
        print(self.adventurer, "\n")
        print(self.dungeon)
        print("\n")

        self.current_room = random.sample(self.dungeon.rooms, k=1)[0]

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

    def move_rooms(self) -> bool:
        move_options = f"""\nWhich direction would you like to move?\n\t1. North\n\t2. East\n\t3. South\n\t4. West\n"""
        move_keys = {"1": "North", "2": "East", "3": "South", "4": "West"}
        user_move_choice = input(move_options)

        while user_move_choice not in ["1", "2", "3", "4"]:
            user_move_choice = input(move_options)
        move_direction = move_keys[user_move_choice]
        if self.current_room.doors[move_direction] is not False:
            self.current_room = self.current_room.doors[move_direction]
            print("\\nYou have entered a new room.")
            return True
        else:
            print(f"\\nThere is no room to the {move_keys[user_move_choice]}")
            return False

    def check_room_content(self):
        if len(self.current_room.content.keys()) == 0:
            print(f"\\nThe current room is empty")
        if "health potion" in self.current_room.content.keys():
            self.pick_up_health_potion(self.current_room.content["health potion"])
            self.current_room.content.pop("health potion")
        if "vision potion" in self.current_room.content.keys():
            self.pick_up_vision_potion()
            self.current_room.content.pop("vision potion")
        if "game_objective" in self.current_room.content.keys():
            self.pick_up_pillar(self.current_room.content["game_objective"])
            self.current_room.content.pop("game_objective")
        if "pit" in self.current_room.content.keys():
            self.fall_in_pit(self.current_room.content["pit"])

    def pick_up_health_potion(self, potion_value: int):
        self.adventurer.add_to_inventory("health potion", potion_value)
        print(
            f"\\nYou found a Health Potion worth {potion_value} health points in the Room. It has been added to your inventory."
        )

    def pick_up_vision_potion(self, potion_value: bool = True):
        self.adventurer.add_to_inventory("vision potion", potion_value)
        print(
            f"You found a Vision Potion in the room. It has been added to your inventory."
        )

    def pick_up_pillar(self, pillar_name: str):
        self.adventurer.add_to_inventory("pillar", pillar_name)
        print(
            f"You found {pillar_name} in the Room! It has been added to your inventory"
        )
        # TODO: Print message about the pillars you still need to find.

    def fall_in_pit(self, pit_value: int):
        print(
            f"You fell in a pit! You lost {pit_value} health points! Your current health score is: {self.adventurer.health_score}"
        )
        self.adventurer.decrease_health(pit_value)

    def _check_player_health(self) -> bool:
        """Internal checks to see if the avatar still has health, used to determine
        if the game continues.
        """

        if self.adventurer.health_score == 0:
            return False
        else:
            return True
