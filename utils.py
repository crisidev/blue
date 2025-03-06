import pyxel

from base import TILE_FLOOR, WALL_TILE_X


class Utils:
    def get_tile(self, tile_x: int, tile_y: int) -> tuple[int, int]:
        return pyxel.tilemaps[0].pget(tile_x, tile_y)

    def is_wall(self, x: int, y: int) -> bool:
        tile = self.get_tile(x // 8, y // 8)
        return tile == TILE_FLOOR or tile[0] >= WALL_TILE_X

    def is_colliding(self, x: int, y: int, is_falling: bool) -> bool:
        x1 = pyxel.floor(x) // 8
        y1 = pyxel.floor(y) // 8
        x2 = (pyxel.ceil(x) + 7) // 8
        y2 = (pyxel.ceil(y) + 7) // 8
        for yi in range(y1, y2 + 1):
            for xi in range(x1, x2 + 1):
                if self.get_tile(xi, yi)[0] >= WALL_TILE_X:
                    return True
        if is_falling and y % 8 == 1:
            for xi in range(x1, x2 + 1):
                if self.get_tile(xi, y1 + 1) == TILE_FLOOR:
                    return True
        return False

    def push_back(self, x: int, y: int, dx: int, dy: int) -> tuple[int, int]:
        for _ in range(pyxel.ceil(abs(dy))):
            step = max(-1, min(1, dy))
            if self.is_colliding(x, y + step, dy > 0):
                break
            y += step
            dy -= step
        for _ in range(pyxel.ceil(abs(dx))):
            step = max(-1, min(1, dx))
            if self.is_colliding(x + step, y, dy > 0):
                break
            x += step
            dx -= step
        return x, y


utils = Utils()
