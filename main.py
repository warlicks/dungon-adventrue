from dungon.dungeon_adventure import DungeonAdventure


def main():
    d = DungeonAdventure(
        max_rooms=6,
        map_height=5,
        map_width=5,
    )

    d.start_game()

    while d.continue_game:
        action = d.chose_action()
        # print(f"current location is ({d.current_room.x}, {d.current_room.y})")

        if action == 1:
            new_room = d.move_rooms()
            if new_room:
                d.check_room_content()

        elif action == 2:
            d.health_potion()
        elif action == 3:
            """Implement Vision Potion. They can see the dungeon a specified
            height and width around the current room if they have Vision Potion
            in their inventory."""
            if (
                len(d.adventurer.inventory.get("vision potion")) != 0
            ):  # ie if list is not empty
                # if they have the potion, print visual and remove potion
                d.room_vision(vision_potion=True)
                d.adventurer.inventory["vision potion"].pop(
                    0
                )  # removes first vision potion in list
            else:
                print(
                    "Nice try! You can't use a Vision Potion unless it is in your inventory!\n"
                )

        elif action == 4:
            d.adventurer.player_status()

        elif action == 5:
            d.maze_exit_outcome()

        elif action == 10:
            """See the whole dungeon map."""
            d.room_vision(vision_potion=False)

        elif action == 10:
            """See the whole dungeon map."""
            d.room_vision(vision_potion=False)


if __name__ == "__main__":
    main()
