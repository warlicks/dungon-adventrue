import random
import textwrap
from .adventurer import Adventurer
from .dungeon import Dungeon
from dungon import dungeon


class DungeonAdventure:
    def __init__(self, **kwargs) -> None:
        self.dungeon = Dungeon(**kwargs)
        self.adventurer = Adventurer(None)
        self.current_room = None

    def start_game(self):
        print(self._welcome_message())

        # Set Up The Player
        player_name = input(
            "\nAre you brave enough to take on this task? If so please enter your name!\n(Please type your name): "
        )
        self.adventurer.name = player_name

        self.dungeon.generate_dungeon()
        self.current_room = random.sample(self.dungeon.rooms, k=1)[0]
        print(self.dungeon)

        print("\nAs you start your exploration your status is:")
        print(self.adventurer, "\n")

        print("\n")
        print(
            f"* You are starting in a room at ({self.current_room.x}, {self.current_room.y})* "
        )
        self.check_room_content()

    def chose_action(self):
        input_options = textwrap.dedent(
            f"""
                                        
        *******************************************************************************
        What would you like to do now, {self.adventurer.name}?
            1. Explore the Dungeon.
            2. Use A Health Potion.
            3. Use A Vision Potion.
            4. Check My Status.
        (Please enter a number from the menu above):  """
        )
        user_choice = input(input_options)
        while user_choice not in ["1", "2", "3", "4"]:
            user_choice = input(input_options)

        return int(user_choice)

    def move_rooms(self) -> bool:
        move_options = textwrap.dedent(
            f"""
            Which direction would you like to move? 
                1. North
                2. East
                3. South
                4. West
            (Please enter a number from the menu to pick a direction): """
        )
        move_keys = {"1": "North", "2": "East", "3": "South", "4": "West"}
        user_move_choice = input(move_options)

        while user_move_choice not in ["1", "2", "3", "4"]:
            user_move_choice = input(move_options)
        move_direction = move_keys[user_move_choice]
        if self.current_room.doors[move_direction] is not False:
            self.current_room = self.current_room.doors[move_direction]
            print(
                textwrap.dedent(
                    f"""
                  * You have entered a new room located @ {self.current_room.x, self.current_room.y} *"""
                )
            )
            print(self.current_room)
            return True
        else:
            print(
                "\nThe door to the {dir} is blocked.".format(
                    dir=move_keys[user_move_choice]
                )
            )
            return False

    def check_room_content(self):
        if len(self.current_room.content.keys()) == 0:
            print("\nThe current room is empty")
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
            "\nYou found a Health Potion worth {value} health points in the Room. It has been added to your inventory.".format(
                value=potion_value
            )
        )

    def pick_up_vision_potion(self, potion_value: bool = True):
        self.adventurer.add_to_inventory("vision potion", potion_value)
        print(
            "\nYou found a Vision Potion in the room. It has been added to your inventory."
        )

    def pick_up_pillar(self, pillar_name: str):
        self.adventurer.add_to_inventory("pillar", pillar_name)
        print(
            "\n\tYou found {p} in the Room! It has been added to your inventory.".format(
                p=pillar_name
            )
        )
        # TODO: Print message about the pillars you still need to find.

    def fall_in_pit(self, pit_value: int):
        self.adventurer.decrease_health(pit_value)
        print(
            f"You fell in a pit! You lost {pit_value} health points! Your current health score is: {self.adventurer.health_score}"
        )

    def _check_player_health(self) -> bool:
        """Internal checks to see if the avatar still has health, used to determine
        if the game continues.
        """

        if self.adventurer.health_score == 0:
            return False
        else:
            return True

    def _welcome_message(self):

        msg = textwrap.dedent(
            """
        --------------------------------------------------------------------------------
        Welcome to the Dungeon of Perpetual Code Bugs. Your mission is to end         
        the cycle of endless bugs by finding the four pillars of object oriented      
        programming. The four pillars, "Abstraction", "Encapsulation", "Inheritance", 
        and "Polymorphism", are scattered throughout the dungeon.
                                                                                      
        Finding all four objectives will be no easy feat. The maze is full of doors 
        that lead no where and rooms with hidden pits that can fall into. While there 
        are dangers in the maze, there also tools in the maze that can help you. 
        Health potions will repair damage done by pits and vision potions can help you
        navigate the maze!
     
        To win the game you need to find all four pillars and make it to the dungeon's
        exit with your health intact! If you run out of health or exit before finding
        all four pillars you'll be stuck debugging poorly documented issues until the 
        end of time.
        --------------------------------------------------------------------------------
        """
        )

        return msg

    def _print_whole_dungeon(self):
        map_storage = []
        for a in range(1, self.dungeon._map_height):
            if a == 1 or a == self.dungeon._map_height:
                map_storage.append(["   "] * self.dungeon._map_width)
            else:
                for room in self.dungeon.rooms:
                    if room.y == a:
                        map_storage[a - 1][room.x - 1] = str(room)
