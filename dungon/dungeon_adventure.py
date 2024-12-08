import random
import textwrap
from .adventurer import Adventurer
from .dungeon import Dungeon


class DungeonAdventure:
    """Builds Dungeon Adventure which takes in the dungeon, adventurer, and room
     objects and provides users options to interact with them."""
    def __init__(self, **kwargs) -> None:
        self.dungeon = Dungeon(**kwargs)
        self.adventurer = Adventurer(None)
        self.adventurer = Adventurer(None)
        self.current_room = None
        self.continue_game = True

    def start_game(self):
        """Starts the game.

        When the game is started this handles a number of tasks.
        1. Prints a welcome message and explains game.
        2. Takes input from player for avatar name.
        3. Generates a new dungeon.
        4. Displays Avatar status.
        5. Displays Maze status and current room.
        """
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
        print(self.current_room)
        self.check_room_content()

    def chose_action(self):
        """Accepts player choice at the start of each turn.

        The player chose from four displayed options.
        Explore the dungeon, use potions or check their status. If they get an
        additional option if they are in a room with an exit; they can chose to
        use the exit.

        There is a hidden option to display the maze map. If the user inputs 10,
        the maze map will be displayed.
        """
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
        if not self._check_for_exit():
            user_choice = input(input_options)
            while user_choice not in ["1", "2", "3", "4", "10"]:
                user_choice = input(input_options)
        else:
            input_option_with_exit = input_options + "5. Exit the Maze"
            user_choice = input(input_option_with_exit)
            while user_choice not in ["1", "2", "3", "4", "5"]:
                user_choice = input(input_options)

        return int(user_choice)

    def move_rooms(self) -> bool:
        """Accepts player movement choices.
        Presents the player with the option to move North, East, South or West.

        If the selected direction leads to a new room they get a message about
        the new room. If the door is blocked they get a message indicating the
        door was blocked
        """
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
        """Checks the room for any content.

        If content is present in the room it is automatically picked up and
        added to the avatar's inventory.
        """
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
        """Picks up a health potion and adds it to the player inventory.

        Args:
            potion_value (int): The value of the health potion
        """
        self.adventurer.add_to_inventory("health potion", potion_value)
        print(
            "\nYou found a Health Potion worth {value} health points in the Room. It has been added to your inventory.".format(
                value=potion_value
            )
        )

    def pick_up_vision_potion(self, potion_value: bool = True):
        """Picks up a vision potion and adds it to the player inventory.

        Args:
            potion_value (bool, optional): The default vision potion value is True.
        """
        self.adventurer.add_to_inventory("vision potion", potion_value)
        print(
            "\nYou found a Vision Potion in the room. It has been added to your inventory."
        )

    def pick_up_pillar(self, pillar_name: str):
        """Picks up a game objective and adds it to the player inventory.

        Args:
            pillar_name (str): The name of the objective found.
        """
        self.adventurer.add_to_inventory("pillar", pillar_name)
        print(
            "\n\tYou found {p} in the Room! It has been added to your inventory.".format(
                p=pillar_name
            )
        )
        # TODO: Print message about the pillars you still need to find.

    def fall_in_pit(self, pit_value: int):
        """Updates the avatar health when they fall in a pit.

        Args:
            pit_value (int): The health damage of the pit.
        """
        self.adventurer.decrease_health(pit_value)
        print(
            f"You fell in a pit! You lost {pit_value} health points! Your current health score is: {self.adventurer.health_score}"
        )

    def check_player_health(self):
        """Checks to see if the avatar still has health, used to determine
        if the game continues.
        """

        if self.adventurer.health_score == 0:
            self._lose_no_health()
            self.continue_game = False
        else:
            self.continue_game = True

    def room_vision(self, vision_potion=False, num_rm_view=8):
        """Prints a visual representation of the nearest
        num_rm_view (defaults to 8) rooms surrounding current room. Implementation of Vision potion
        which is used to allow user to see eight rooms surrounding current room and current room.
        location in maze may cause less than num_rm_view (defaults to 8) to be displayed.
        """

        if vision_potion is True:
            # set distance on map around current room to print. currently is 4 in either direction
            view_around = round(num_rm_view / 2)

            minx, miny = (
                self.current_room.x - view_around,
                self.current_room.y - view_around,
            )
            maxx, maxy = (
                self.current_room.x + view_around,
                self.current_room.y + view_around,
            )
            minx = max(minx, 0)  # remove negatives
            miny = max(miny, 0)  # remove negatives

        else:
            miny, maxy = 0, self.dungeon._map_height
            minx, maxx = 0, self.dungeon._map_width

        # create a list of rooms to include in our visual based on min and max x and y above
        print_rooms = []
        for room in self.dungeon.rooms:
            if minx <= room.x <= maxx and miny <= room.y <= maxy:
                print_rooms.append(room)

        combined_string = ""

        # print one row at a time. all together will create grid.
        for print_row in range(miny, maxy + 1):
            # each x-coordinate value of 1 (width) gets 3 spaces.
            # each row in dungeon has lines because of stars above and below
            row_str1 = "   " * (maxx - minx + 1)
            row_str2 = "   " * (maxx - minx + 1)
            row_str3 = "   " * (maxx - minx + 1)
            for room in print_rooms:  # check all the rooms to print
                if room.y == print_row:  # if they are in the row
                    # remove \n. makes count hard and changes spacing.
                    rm_str = room.__str__().replace("\n", "")
                    # and splice the current row strings (three lines per print_row)
                    row_str1 = f"{row_str1[:(room.x * 3)]}{rm_str[0:3]}{row_str1[(room.x * 3 + 3) + 1:]}"
                    row_str2 = f"{row_str2[:(room.x * 3)]}{rm_str[3:6]}{row_str2[(room.x * 3 + 3) + 1:]}"
                    row_str3 = f"{row_str3[:(room.x * 3)]}{rm_str[6:9]}{row_str3[(room.x * 3 + 3) + 1:]}"
            print(row_str1)
            print(row_str2)
            print(row_str3)
            combined_string = combined_string + \
                              row_str1 + \
                              row_str2 + \
                              row_str3

        print(f"create visual for {print_rooms}")
        return combined_string

    def health_potion(self):
        """Manages adventurers health potion within their inventory.
        They can use it and if they do it is removed from inventory."""
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
            temp = [str(x) for x in self.adventurer.inventory["health potion"]]
            while potion_value not in temp:
                potion_value = input(input_msg)

            # Remove from inventory
            self.adventurer.remove_from_inventory("health potion", int(potion_value))
            self.adventurer.increase_health(int(potion_value))
            print(f"Your health has increased to {self.adventurer.health_score}")

    def _check_for_exit(self) -> bool:
        """Internal method to check if the room has a maze exit.

        This method is used to present users with an option to exit the maze
        when they are in the room with the exit.


        Returns:
            bool: Indicates if an exit is present.
        """
        if "exit" in self.current_room.content.keys():
            return True
        else:
            return False

    def maze_exit_outcome(self):
        """Checks if the player has won when they exit the maze.

        To win the the player must have all the game objectives when they exit
        the dungeon.
        """
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
        """Internal method prints message when you win the game."""
        print("You Win!")
        print(
            "You've ended cycle of endless bugs by finding the four pillars of object oriented programming."
        )

    def _lose_maze_exit(self):
        """Internal method generate message if you lose the game b/c of exiting the maze early."""
        missing = [
            x
            for x in ["Abstraction", "Encapsulation", "Inheritance", "Polymorphism"]
            if x not in self.adventurer.inventory["pillar"]
        ]
        print(
            "\nYou'll be stuck debugging poorly documented issues until the end of time! You left the maze without finding\n"
        )
        print("\n".join(missing))

    def _lose_no_health(self):
        """Internal method generates message if you lose the game because of no health."""
        print(
            "You Died Dungeon of Perpetual Code Bugs!\n The Dungeon is a dangerous place. Play again; if you are brave enough!"
        )

    def _welcome_message(self):
        """Internal method that prints the message at the start of the game."""
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

        HOW TO PLAY

        With each turn you will have the option to 1) Explore the maze,
        2) Use a health potion, 3) Use a vision potion or 4) Check your status.

        If you choose to explore the maze you will be asked which direction
        (North, East, South, or West) you want to explore. If you find a new room,
        any objects in the room will automatically be picked up. Likewise if you come
        across a pit, you will fall in, destined to forever be trapped in a maze
        of incomprehensible classes, and methods, and constructors (oh my!).

        If you choose to use a health potion your health will increase by the
        value of the potion and the potion will be removed from your inventory.
        If you choose to use a vision potion you will be able to see part of the
        dungeon around you.

        To win the game you need to find all four pillars and make it to the dungeon's
        exit with your health intact! If you run out of health or exit before finding
        all four pillars you'll be stuck debugging poorly documented issues until the
        end of time.
        --------------------------------------------------------------------------------
        """
        )

        print(msg)
