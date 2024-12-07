import random
from .adventurer import Adventurer
from .dungeon import Dungeon


class DungeonAdventure:
    def __init__(self, **kwargs) -> None:
        self.dungeon = Dungeon(**kwargs)
        self.adventurer = Adventurer(None)
        self.current_room = None
        self.continue_game = True

    def start_game(self):
        # TODO: Print Welcome Message.

        # Set Up The Player
        player_name = input("Brave Explorer, what is your name?\n\tEnter Your Name: ")
        self.adventurer.name = player_name

        self.dungeon.generate_dungeon()
        self.current_room = random.sample(self.dungeon.rooms, k=1)[0]

        print(f"Welcome to the Dungeon {self.adventurer.name}.\n")
        print("As you start your exploration your status is:\n")
        print(self.adventurer, "\n")
        print(self.dungeon)
        print("\n")
        print(
            f"You are starting in a room at {self.current_room.x}, {self.current_room.y}"
        )
        self.check_room_content()

    def chose_action(self):
        input_options = f"""What would you like to do now, {self.adventurer.name}?
        Please Enter A Number from the Menu Below.
        1. Explore the Dungeon.
        2. Use A Health Potion.
        3. Use A Vision Potion.
        4. Check My Status.
        """
        if not self._check_for_exit():
            user_choice = input(input_options)
            while user_choice not in ["1", "2", "3", "4"]:
                user_choice = input(input_options)
        else:
            input_option_with_exit = input_options + "5. Exit the Maze"
            user_choice = input(input_option_with_exit)
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
            print(
                f"\\nYou have entered a new room located @ {self.current_room.x, self.current_room.y}"
            )
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

    def check_player_health(self):
        """Checks to see if the avatar still has health, used to determine
        if the game continues.
        """

        if self.adventurer.health_score == 0:
            self._lose_no_health()
            self.continue_game = False
        else:
            self.continue_game = True

    def room_vision(self, num_rm_view=8):
        """Prints a visual representation of the nearest
        num_rm_view (defaults to 8) rooms surrounding current room. Implementation of Vision potion
        which is used to allow user to see eight rooms surrounding current room and current room.
        location in maze may cause less than num_rm_view (defaults to 8) to be displayed.
        """

        # note: we need to know what the current room is, so I imported dungeon_adventure from dungon
        # dungeon_adventure.current_room <-- note, we don't need the actual object can just use coordinates?

        # from dungon.room import Room
        # Room._room_content_string()
        view_around = round(num_rm_view / 2)

        minx, miny = (
            self.current_room.x - view_around,
            self.current_room.y - view_around,
        )
        maxx, maxy = (
            self.current_room.x + view_around,
            self.current_room.y + view_around,
        )

        print(
            f"The view in the grid between: bottom left ({minx}, {miny}), \n "
            f"bottom right ({minx}, {maxy}), \n"
            f"top left ({maxx}, {miny}), \n"
            f"top right ({maxx}, {maxy}):"
        )

        print_rooms = []
        for room in self.dungeon.rooms:
            if minx <= room.x <= maxx and miny <= room.y <= maxy:
                print_rooms.append(room)
                print(f"adding {room} to print out list")

        print(f"create visual for {print_rooms}")

    def health_potion(self):
        if not self.adventurer.inventory["health potion"]:
            print("You don't have any health potion to use")
        else:
            input_msg = (
                "Which health potion would you like to use?"
                + "\n".join(  # Need str(x) b/c join won't work w/ the int value in the list
                    [str(x) for x in self.adventurer.inventory["health potion"]]
                )
                + "Please enter the value of the potion you would like to use: "
            )
            potion_value = input(input_msg)
            while (
                int(potion_value) not in self.adventurer.inventory["health potion"]
                or not potion_value.isnumeric()
            ):
                potion_value = input(input_msg)

            # Remove from inventory
            self.adventurer.remove_from_inventory("health potion", int(potion_value))
            self.adventurer.increase_health(int(potion_value))
            print(f"Your health has increased to {self.adventurer.health_score}")

    def _check_for_exit(self) -> bool:
        if "exit" in self.current_room.content.keys():
            return True
        else:
            return False

    def maze_exit_outcome(self):
        present = [
            x in self.adventurer.inventory["pillar"]
            for x in ["Abstraction", "Encapsulation", "Inheritance", "Polymorphism"]
        ]

        if all(present):
            self._winning_message()
            self.continue_game = False
        else:
            self._lose_maze_exit()
            self.continue_game = False

    def _winning_message(self):
        print("You Win!")

    def _lose_maze_exit(self):
        missing = [
            x
            for x in ["Abstraction", "Encapsulation", "Inheritance", "Polymorphism"]
            if x not in self.adventurer.inventory["pillar"]
        ]
        print("You left the maze without finding")
        print("\n".join(missing))

    def _lose_no_health(self):
        print(
            "You Died Dungeon of Perpetual Code Bugs!\n The Dungeon is a dangerous place. Play again; if you are brave enough!"
        )
