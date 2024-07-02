from src.utils.texture import Animation
import pygame as pg
from math import pi, atan2, sin, cos, radians
from src.utils.constants import WIDTH, HEIGHT


class Player(Animation):
    def __init__(self, position):
        super().__init__(position, 'assets/textures/spritesheets/spaceship.png', (32, 32), 2)

        self.hitbox_radius = 25
        self.rotation = 0

        self.velocity = pg.Vector2()
        self.acceleration = 10
        self.max_speed = 20

        self.spawn_laser = False

        self.angular_velocity = 180  # degrees per sec

        self.laser_cooldown = 0
        self.cd = 0.2

    def update(self, *args):
        dt = args[0]
        mouse_pos = args[1]
        scroll = args[2]
        keys_pressed = args[3]
        cursor = args[4]

        super().update(dt)

        # updating the rotation
        if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]:
            self.rotation += self.angular_velocity * dt

        if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]:
            self.rotation -= self.angular_velocity * dt


        # updating the position
        if (keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]) and self.velocity.magnitude() < self.max_speed//2:
            self.velocity.x += cos(radians(self.rotation))*self.acceleration * dt
            self.velocity.y -= sin(radians(self.rotation))*self.acceleration * dt


        if keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s] or keys_pressed[pg.K_SPACE] or keys_pressed[pg.KMOD_SHIFT]:
            self.velocity /= 1.1

        self.velocity = self.velocity.clamp_magnitude(self.max_speed)

        self.position[0] += self.velocity.x
        self.position[1] += self.velocity.y

        new_scroll = self.position.lerp(pg.Vector2(scroll)+pg.Vector2(mouse_pos)-pg.Vector2(WIDTH//2, HEIGHT//2), 0.2)
        scroll[0] = new_scroll[0]
        scroll[1] = new_scroll[1]


        # spawning lasers
        if cursor.holding and self.laser_cooldown < 0:
            self.spawn_laser = True
            self.laser_cooldown = self.cd
        else:
            self.spawn_laser = False
            self.laser_cooldown -= dt

    def draw(self, *args):
        surf = args[0]
        scroll = args[1]
        super().draw(surf, scroll, self.rotation-90, 2)
