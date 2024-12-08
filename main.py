from dungon.dungeon_adventure import DungeonAdventure


def play_game():
    d = DungeonAdventure(
        max_rooms=6,
        map_height=5,
        map_width=5,
    )

    d.start_game()

    while d.continue_game:
        """Take the inputs provided by user and initiate actions."""
        action = d.chose_action()
        # print(f"current location is ({d.current_room.x}, {d.current_room.y})")

        if action == 1:
            """Adventurer will move rooms based on user input and 
             the current dungeon map. Options to move N, E, S or W are given."""
            new_room = d.move_rooms()
            if new_room:
                d.check_room_content()
        elif action == 2:
            """Adventurer uses a health potion it is available."""
            d.health_potion()
        elif action == 3:
            """Implement Vision Potion. They can see the dungeon a specified
            height and width around the current room if they have Vision Potion
            in their inventory."""
            if (
                len(d.adventurer.inventory.get("vision potion")) != 0
            ):
                d.room_vision(vision_potion=True)
                d.adventurer.inventory["vision potion"].pop(
                    0
                )  # removes first vision potion in list
            else:
                print(
                    "Nice try! You can't use a Vision Potion unless it is in your inventory!\n"
                )

        elif action == 4:
            """Prints out player's status."""
            d.adventurer.player_status()

        elif action == 5:
            "Exit the maze."
            d.maze_exit_outcome()

        elif action == 10:
            """See the whole dungeon map."""
            d.room_vision(vision_potion=False)


if __name__ == "__main__":
    play_game()
