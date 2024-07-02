from src.utils.texture import Animation
import pygame as pg
from math import pi, atan2, sin, cos, radians, degrees, sqrt
from src.utils.constants import WIDTH, HEIGHT
import random



class Enemy(Animation):
    def __init__(self, position):
        super().__init__(position, 'assets/textures/spritesheets/enemy-spaceship.png', (32, 32), 2)

        self.hitbox = pg.Rect(position, (50, 50))
        self.rotation = 0

        self.velocity = pg.Vector2()
        self.acceleration = 10
        self.max_speed = 7

        self.spawn_laser = False

        self.angular_velocity = 180  # degrees per sec

        self.laser_cooldown = 0
        self.cd = 1

        self.in_pursuit = False

    def update(self, *args):
        dt = args[0]
        player_pos = args[1]

        super().update(dt)

        # updating the rotation
        target_rotation = 180+degrees(atan2(-self.position.y+player_pos.y, self.position.x-player_pos.x))

        self.rotation = self.rotation % 360
        target_rotation = target_rotation % 360

        # Calculate the differences in both directions
        clockwise_diff = (target_rotation - self.rotation) % 360
        counterclockwise_diff = (self.rotation - target_rotation) % 360

        if self.in_pursuit is False:
            pass
        elif clockwise_diff <= counterclockwise_diff and abs(clockwise_diff) > 2:
            self.rotation += self.angular_velocity * dt
        elif counterclockwise_diff < clockwise_diff and abs(counterclockwise_diff) > 2:
            self.rotation -= self.angular_velocity * dt


        # updating the position
        distance_to_player = sqrt((self.position.x-player_pos.x)**2+(self.position.y-player_pos.y)**2)

        if distance_to_player < 400:
            self.in_pursuit = True

        if distance_to_player > 300 and self.in_pursuit:
            rotation = random.randint(-100, 100) + self.rotation
            self.velocity.x += cos(radians(rotation)) * self.acceleration * dt
            self.velocity.y -= sin(radians(rotation)) * self.acceleration * dt

            self.velocity = self.velocity.clamp_magnitude(self.max_speed)
        else:
            self.velocity /= 1.1


        self.position[0] += self.velocity.x
        self.position[1] += self.velocity.y

        # spawning lasers
        if distance_to_player < 400 and self.laser_cooldown < 0:
            self.spawn_laser = True
            self.laser_cooldown = self.cd + random.randint(0, 3000)/1000
        else:
            self.spawn_laser = False
            self.laser_cooldown -= dt


    def draw(self, *args):
        surf = args[0]
        scroll = args[1]
        super().draw(surf, scroll, self.rotation-90, 2)
