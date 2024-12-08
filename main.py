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
            d.room_vision()
        elif action == 4:
            d.adventurer.player_status()
        elif action == 10:
            d.dungeon.print_dungeon_map()
        elif action == 5:
            d.maze_exit_outcome()


if __name__ == "__main__":
    main()
