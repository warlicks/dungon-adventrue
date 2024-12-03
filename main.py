from dungon.dungeon_adventure import DungeonAdventure


def main():
    d = DungeonAdventure()

    d.start_game()

    for i in range(4):
        action = d.chose_action()

        if action == 1:
            new_room = d.move_rooms()
            if new_room:
                d.check_room_content()
        elif action == 2:
            print("HEALTH POTION NOT IMPLEMENTED")
        elif action == 3:
            print("VISION POTION NOT IMPLEMENTED")
        elif action == 4:
            d.adventurer.player_status()


if __name__ == "__main__":
    main()
