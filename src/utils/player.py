from src.utils.texture import Animation
import pygame as pg
from math import pi, atan2, sin, cos, radians
from src.utils.constants import WIDTH, HEIGHT


class Player(Animation):
    def __init__(self, position):
        super().__init__(position, 'assets/textures/spritesheets/spaceship.png', (32, 32), 2)

        self.hitbox = pg.Rect(position, (50, 50))
        self.rotation = 0

        self.velocity = pg.Vector2()
        self.acceleration = 10
        self.max_speed = 1

    def update(self, *args):
        dt = args[0]
        mouse_pos = args[1]
        scroll = args[2]
        keys_pressed = args[3]

        super().update(dt)

        vector_from_player_to_mouse = pg.Vector2(mouse_pos[0] + scroll[0] - WIDTH // 2 - self.position.x, mouse_pos[1] + scroll[1] - HEIGHT // 2 - self.position.y)

        self.rotation = 180 / pi * atan2(-vector_from_player_to_mouse.y, vector_from_player_to_mouse.x)
        if self.rotation < 0:
            self.rotation += 2 * pi


        if keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]:
            self.velocity.x += cos(radians(self.rotation))*self.acceleration * dt
            self.velocity.y -= sin(radians(self.rotation))*self.acceleration * dt

            self.velocity.clamp_magnitude(self.max_speed)


        self.position[0] += self.velocity.x
        self.position[1] += self.velocity.y

        scroll[0] -= (scroll[0] - self.position[0])/10
        scroll[1] -= (scroll[1] - self.position[1]) / 10

    def draw(self, *args):
        surf = args[0]
        scroll = args[1]
        super().draw(surf, scroll, self.rotation-90, 2)
