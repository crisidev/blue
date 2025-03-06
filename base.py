from typing_extensions import Self

TRANSPARENT_COLOR = 2
SCROLL_BORDER_X = 80
TILE_FLOOR = (1, 0)
TILE_SPAWN1 = (0, 1)
TILE_SPAWN2 = (1, 1)
TILE_SPAWN3 = (2, 1)
WALL_TILE_X = 4


class Entity:
    def __init__(self, x: int, y: int, is_alive: bool = True) -> None:
        self.x: int = x
        self.y: int = y
        self.is_alive: bool = is_alive

    def update(self, entities: list[Self]): ...
    def draw(self): ...
