from typing import override

import pyxel

from base import TRANSPARENT_COLOR, Entity
from utils import utils


class Enemy(Entity): ...


class Enemy1(Enemy):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.dx: int = 0
        self.dy: int = 0
        self.direction: int = -1

    @override
    def update(self, entities: list[Entity]):
        self.dx = self.direction
        self.dy = min(self.dy + 1, 3)
        if self.direction < 0 and utils.is_wall(self.x - 1, self.y + 4):
            self.direction = 1
        elif self.direction > 0 and utils.is_wall(self.x + 8, self.y + 4):
            self.direction = -1
        self.x, self.y = utils.push_back(self.x, self.y, self.dx, self.dy)

    @override
    def draw(self):
        u = pyxel.frame_count // 4 % 2 * 8
        w = 8 if self.direction > 0 else -8
        pyxel.blt(self.x, self.y, 0, u, 24, w, 8, TRANSPARENT_COLOR)


class Enemy2(Enemy):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.dx: int = 0
        self.dy: int = 0
        self.direction: int = -1

    @override
    def update(self, entities: list[Entity]):
        self.dx = self.direction
        self.dy = min(self.dy + 1, 3)
        if utils.is_wall(self.x, self.y + 8) or utils.is_wall(self.x + 7, self.y + 8):
            if self.direction < 0 and (
                utils.is_wall(self.x - 1, self.y + 4) or not utils.is_wall(self.x - 1, self.y + 8)
            ):
                self.direction = 1
            elif self.direction > 0 and (
                utils.is_wall(self.x + 8, self.y + 4) or not utils.is_wall(self.x + 7, self.y + 8)
            ):
                self.direction = -1
        self.x, self.y = utils.push_back(self.x, self.y, self.dx, self.dy)

    @override
    def draw(self):
        u = pyxel.frame_count // 4 % 2 * 8 + 16
        w = 8 if self.direction > 0 else -8
        pyxel.blt(self.x, self.y, 0, u, 24, w, 8, TRANSPARENT_COLOR)


class Enemy3(Enemy):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.time_to_fire: int = 0

    @override
    def update(self, entities: list[Entity]):
        self.time_to_fire -= 1
        if self.time_to_fire <= 0:
            dx = player.x - self.x
            dy = player.y - self.y
            sq_dist = dx * dx + dy * dy
            if sq_dist < 60**2:
                dist = pyxel.sqrt(sq_dist)
                entities.append(Enemy3Bullet(self.x, self.y, dx / dist, dy / dist))
                self.time_to_fire = 60

    @override
    def draw(self):
        u = pyxel.frame_count // 8 % 2 * 8
        pyxel.blt(self.x, self.y, 0, u, 32, 8, 8, TRANSPARENT_COLOR)


class Enemy3Bullet(Entity):
    def __init__(self, x: int, y: int, dx: float, dy: float) -> None:
        super().__init__(x, y)
        self.dx: int = int(dx)
        self.dy: int = int(dy)

    @override
    def update(self, entities: list[Entity]):
        self.x += self.dx
        self.y += self.dy

    @override
    def draw(self):
        u = pyxel.frame_count // 2 % 2 * 8 + 16
        pyxel.blt(self.x, self.y, 0, u, 32, 8, 8, TRANSPARENT_COLOR)
