# title: Pyxel Platformer
# author: Takashi Kitao
# desc: A Pyxel platformer example
# site: https://github.com/kitao/pyxel
# license: MIT
# version: 1.0

import builtins

import pyxel
from typing_extensions import override

from base import SCROLL_BORDER_X, TILE_SPAWN1, TILE_SPAWN2, TILE_SPAWN3, TRANSPARENT_COLOR, Entity
from enemies import Enemy1, Enemy2, Enemy3
from utils import utils


def spawn_enemy(left_x: int, right_x: int, enemies: list[Entity]):
    left_x = pyxel.ceil(left_x / 8)
    right_x = pyxel.floor(right_x / 8)
    for x in range(left_x, right_x + 1):
        for y in range(16):
            tile = utils.get_tile(x, y)
            if tile == TILE_SPAWN1:
                enemies.append(Enemy1(x * 8, y * 8))
            elif tile == TILE_SPAWN2:
                enemies.append(Enemy2(x * 8, y * 8))
            elif tile == TILE_SPAWN3:
                enemies.append(Enemy3(x * 8, y * 8))


scroll_x = 0


class Player(Entity):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.dx: int = 0
        self.dy: int = 0
        self.direction: int = 1
        self.is_falling: bool = False

    @override
    def update(self, entities: list[Entity]):
        global scroll_x
        last_y = self.y
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.dx = -2
            self.direction = -1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.dx = 2
            self.direction = 1
        self.dy = min(self.dy + 1, 3)
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.dy = -6
            pyxel.play(3, 8)
        self.x, self.y = utils.push_back(self.x, self.y, self.dx, self.dy)
        if self.x < scroll_x:
            self.x = scroll_x
        if self.y < 0:
            self.y = 0
        self.dx = int(self.dx * 0.8)
        self.is_falling = self.y > last_y

        if self.x > scroll_x + SCROLL_BORDER_X:
            last_scroll_x = scroll_x
            scroll_x = min(self.x - SCROLL_BORDER_X, 240 * 8)
            spawn_enemy(last_scroll_x + 128, scroll_x + 127, entities)
        if self.y >= pyxel.height:
            raise ValueError

    @override
    def draw(self):
        u = (2 if self.is_falling else pyxel.frame_count // 3 % 2) * 8
        w = 8 if self.direction > 0 else -8
        pyxel.blt(self.x, self.y, 0, u, 16, w, 8, TRANSPARENT_COLOR)


player = Player(0, 0)
setattr(builtins, "player", player)


class App:
    def __init__(self):
        self.enemies: list[Entity] = []
        pyxel.init(128, 128, title="Pyxel Platformer")
        pyxel.load("assets/platformer.pyxres")
        # Change enemy spawn tiles invisible
        pyxel.images[0].rect(0, 8, 24, 8, TRANSPARENT_COLOR)
        spawn_enemy(0, 127, self.enemies)
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    @staticmethod
    def cleanup_entities(entities: list[Entity]) -> None:
        for i in range(len(entities) - 1, -1, -1):
            if not entities[i].is_alive:
                del entities[i]

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        try:
            player.update(self.enemies)
        except ValueError:
            self.game_over()
            return

        for enemy in self.enemies:
            if abs(player.x - enemy.x) < 6 and abs(player.y - enemy.y) < 6:
                self.game_over()
                return
            enemy.update(self.enemies)
            if enemy.x < scroll_x - 8 or enemy.x > scroll_x + 160 or enemy.y > 160:
                enemy.is_alive = False
        self.cleanup_entities(self.enemies)

    def draw(self):
        pyxel.cls(0)

        # Draw level
        pyxel.camera()
        pyxel.bltm(0, 0, 0, (scroll_x // 4) % 128, 128, 128, 128)
        pyxel.bltm(0, 0, 0, scroll_x, 0, 128, 128, TRANSPARENT_COLOR)

        # Draw characters
        pyxel.camera(scroll_x, 0)
        player.draw()
        for enemy in self.enemies:
            enemy.draw()

    def game_over(self):
        global scroll_x
        scroll_x = 0
        player.x = 0
        player.y = 0
        player.dx = 0
        player.dy = 0
        self.enemies = []
        spawn_enemy(0, 127, self.enemies)
        pyxel.play(3, 9)


if __name__ == "__main__":
    _ = App()
