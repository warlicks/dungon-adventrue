class Room:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.doors = {"North": False, "East": False, "South": False, "West": False}
