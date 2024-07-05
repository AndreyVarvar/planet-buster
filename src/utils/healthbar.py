import pygame as pg

from src.utils.thingy import Thingy


class HealthBar(Thingy):
    def __init__(self, position, sprite_manager):
        sprite_manager.add('health bar', 'assets/textures/sprites/health-bar.png', True, (64, 16))

        self.bar = sprite_manager.sprites['health bar']
        self.bar_state = 4

        super().__init__(position, self.bar[4-self.bar_state], scale=1.5)

        self.depleted = False

    def decrease(self):
        if self.bar_state > 0:
            self.bar_state -= 1
            self.texture = self.bar[4-self.bar_state]

        if self.bar_state == 0:
            self.depleted = True

    def draw(self, surf, scroll, offset=pg.Vector2(0, 0)):
        self.texture = self.bar[4 - self.bar_state]
        super().draw(surf, scroll, offset)
