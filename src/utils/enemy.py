from src.utils.texture import Animation
from math import atan2, sin, cos, radians, degrees, sqrt
import random
from src.utils.constants import *


class Enemy(Animation):
    def __init__(self, position):
        super().__init__(position, 'assets/textures/spritesheets/enemy-spaceship.png', (32, 32), 2)

        self.hitbox_radius = 50
        self.rotation = 0

        self.velocity = pg.Vector2()
        self.acceleration = 10
        self.max_speed = 20

        self.dead = False
        self.playing_animation = False
        self.really_dead_and_should_be_destroyed = False

        self.spawn_laser = False

        self.angular_velocity = 180  # degrees per sec

        self.laser_cooldown = 0
        self.cd = 1

        self.in_pursuit = False
        self.close_to_crashing = False

    def update(self, *args):
        dt = args[0]
        player_pos = args[1]
        map_boundaries = args[2]
        scroll = args[3]

        super().update(dt)

        if not self.dead:

            # updating the rotation
            target_rotation = 180+degrees(atan2(-self.position.y+player_pos.y, self.position.x-player_pos.x))

            self.rotation = self.rotation % 360
            target_rotation = target_rotation % 360

            # Calculate the differences in both directions
            clockwise_diff = (target_rotation - self.rotation) % 360
            counterclockwise_diff = (self.rotation - target_rotation) % 360

            # pursuit the player if spotted
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

            if (distance_to_player > 300 and self.in_pursuit) and self.velocity.magnitude() < self.max_speed//2:
                rotation = random.randint(-100, 100) + self.rotation
                self.velocity.x += cos(radians(rotation)) * self.acceleration * dt
                self.velocity.y -= sin(radians(rotation)) * self.acceleration * dt
            else:
                self.velocity /= 1.1

            self.velocity = self.velocity.clamp_magnitude(self.max_speed)

            self.position[0] += self.velocity.x
            self.position[1] += self.velocity.y

            # spawning lasers
            if distance_to_player < 500 and self.laser_cooldown < 0 and self.in_pursuit:
                self.spawn_laser = True
                self.laser_cooldown = self.cd + random.randint(0, 3000)/1000
            else:
                self.spawn_laser = False
                self.laser_cooldown -= dt

            # make sure we don't leave out of bounds
            if (self.position.x-self.hitbox_radius) < map_boundaries.left:
                self.velocity.x = 0
                self.position.x = map_boundaries.left + self.hitbox_radius
            elif (self.position.x+self.hitbox_radius) > map_boundaries.right:
                self.velocity.x = 0
                self.position.x = map_boundaries.right - self.hitbox_radius

            if (self.position.y - self.hitbox_radius) < map_boundaries.top:
                self.velocity.y = 0
                self.position.y = map_boundaries.top + self.hitbox_radius
            elif (self.position.y + self.hitbox_radius) > map_boundaries.bottom:
                self.velocity.y = 0
                self.position.y = map_boundaries.bottom - self.hitbox_radius

        # switch to dead
        else:
            if self.playing_animation is False:  # just died
                scroll[0] += random.randint(-100, 100)
                scroll[1] += random.randint(-100, 100)

                random.choice(explosion).play()

                self.playing_animation = True
                self.rotation = 0
                super().__init__(self.position, 'assets/textures/spritesheets/explosion.png', (96, 96), 5, 1)

            if self.animation_end:
                self.really_dead_and_should_be_destroyed = True


    def draw(self, *args):
        surf = args[0]
        scroll = args[1]
        time = args[2]
        super().draw(surf, scroll, self.rotation-90, 2, angle=time, strength=2)
