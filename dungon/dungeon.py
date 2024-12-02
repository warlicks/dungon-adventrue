import random
from typing import List
from .room import Room


class Dungeon:
    def __init__(
        self, max_rooms: int = 10, map_height: int = 50, map_width: int = 50
    ) -> None:
        self._max_rooms = max_rooms
        self._map_height = map_height
        self._map_width = map_width
        self.rooms = []

    def generate_dungeon(self) -> None:
        num_rooms = 0
        for r in range(self._max_rooms):
            new_room = Room(
                random.randint(1, self._map_width), random.randint(1, self._map_height)
            )

            if num_rooms == 0:
                # Assign the first room created as the entrance
                new_room.generate_room_content("entrance", True, 1.0)

            else:
                # Make connection to previous room
                previous_room = self.rooms[num_rooms - 1]
                self._connect_rooms(new_room, previous_room)

                # Do room content creation.
                # If it is the last room assign an exit and nothing else.
                if num_rooms == (self._max_rooms - 1):
                    new_room.generate_room_content("exit", True, 1.0)
                else:
                    new_room.generate_pit()
                    new_room.generate_healing_potion()
                    new_room.generate_room_content("vision potion", True)

            self.rooms.append(new_room)
            num_rooms += 1
        # Do Pillar Placement
        # TODO: Make this more modular. Objectives should be a argument somewhere.
        self._place_game_objectives(
            ["Abstraction", "Encapsulation", "Inheritance", "Polymorphism"]
        )
        self.maze_status()

    def _connect_rooms(self, new_room: Room, previous_room: Room):
        """Connects the newly created to the previous room.

        The room connections are made based on the concepts of tunnels between the rooms.
        The "tunnel path" is randomly decided and the doors of the two rooms are
        connected based on the "path" taken between the two rooms.

        If the new room is NE of the old room we could draw the tunnel in two ways. The
        tunnel could be dug east first and then north, entering from the south of the new room.
        The other option would be to dig north and then east, entering the east side of
        new room.

        Args:
            new_room (Room): The newly created room object. It will be connected to the
              previous room based on it's relative location and the "tunnel path"
            previous_room (Room): An existing room. It is connected to the new room
              based on the relative location and the "tunnel path" between the rooms.
        """

        # decide if the "tunnel" will go vertical or horizontal first.
        path = self._decide_connection_path()

        # Location 1: New room is SE of previous room.
        if previous_room.x < new_room.x and previous_room.y > new_room.y:
            self._assign_doors(
                path, previous_room, new_room, "East", "North", "South", "West"
            )

        # Location 2: New room NE of pervious room
        elif previous_room.x < new_room.x and previous_room.y < new_room.y:
            self._assign_doors(
                path, previous_room, new_room, "East", "South", "North", "West"
            )

        # Location 3: New Room NW of previous room
        elif previous_room.x > new_room.x and previous_room.y < new_room.y:
            self._assign_doors(
                path, previous_room, new_room, "West", "South", "North", "East"
            )

        # Location 4: New Room SW of previous room
        elif previous_room.x > new_room.x and previous_room.y > new_room.y:
            self._assign_doors(
                path, previous_room, new_room, "West", "North", "South", "East"
            )

        # Location 5: New Room N of previous room
        elif previous_room.x == new_room.x and previous_room.y < new_room.y:
            previous_room.doors["North"] = new_room
            new_room.doors["South"] = previous_room

        # Location 6: New Room S of Previous room.
        elif previous_room.x == new_room.x and previous_room.y > new_room.y:
            previous_room.doors["South"] = new_room
            new_room.doors["North"] = previous_room

        # Location 7 : New Room E of previous room
        elif previous_room.x < new_room.x and previous_room.y == new_room.y:
            previous_room.doors["East"] = new_room
            new_room.doors["West"] = previous_room

        # Location 7 : New Room W of previous room
        elif previous_room.x > new_room.x and previous_room.y == new_room.y:
            previous_room.doors["West"] = new_room
            new_room.doors["East"] = previous_room

    def _decide_connection_path(self):
        """Internal method to decide if the path between to rooms will
        go horizontal or vertical first.
        """
        if random.randint(0, 1) == 1:
            return "H"
        else:
            return "V"

    # TODO: Should this be internal or external? Should this live here or in dungeon_adventure?
    # This should be modular enough to pick it up and move it with minimal changes.
    def _place_game_objectives(self, objectives: List[str]) -> None:

        num_objectives = len(objectives)

        # We do -2 because we can't place things in the entrance or exit rooms.
        if num_objectives > len(self.rooms) - 2:
            raise ValueError(
                "You can't place all of your objectives. There aren't enough eligible rooms"
            )

        object_rooms = random.sample(self.rooms[1:-1], k=num_objectives)
        for obj in objectives:
            for r in object_rooms:
                r.generate_room_content("game_objective", obj, 1.0)

    def _assign_doors(
        self,
        path: str,
        previous_room: Room,
        new_room: Room,
        previous_horizontal_door: str,
        new_horizontal_door: str,
        previous_vertical_door: str,
        new_vertical_door: str,
    ):
        # TODO: Add A check that the door strings are valid. Should be North, East, South, West.
        if path == "H":
            # Check to make sure the door isn't in use already. If in use go other path.
            if previous_room.doors[previous_horizontal_door] is False:
                previous_room.doors[previous_horizontal_door] = new_room
                new_room.doors[new_horizontal_door] = previous_room
            else:
                previous_room.doors[previous_vertical_door] = new_room
                new_room.doors[new_vertical_door] = previous_room
        else:
            if previous_room.doors[previous_vertical_door] is False:
                previous_room.doors[previous_vertical_door] = new_room
                new_room.doors[new_vertical_door] = previous_room
            else:
                previous_room.doors[previous_horizontal_door] = new_room
                new_room.doors[new_horizontal_door] = previous_room

    def maze_status(self):

        self.object_counts = {}

        # Find all the items in the maze
        for r in self.rooms:
            for key in r.content.keys():
                if key in self.object_counts.keys():
                    self.object_counts[key] += 1
                else:
                    self.object_counts[key] = 1

    def __str__(self):
        content_list = [f"{k}: {v}" for k, v in self.object_counts.items()]
        content_str = "\n\t".join(content_list)
        msg = f"The Maze is deep and twisting. There are {len(self.rooms)} rooms to explore and survive.\n\nHidden in the maze, you can find:\n\t{content_str}."

        return msg
