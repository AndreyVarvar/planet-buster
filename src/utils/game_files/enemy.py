from src.utils.animation import Animation
from math import atan2, sin, cos, radians, degrees, sqrt
import random
from src.utils.constants import *
from src.utils.game_files.healthbar import HealthBar


class Enemy(Animation):
    def __init__(self, position, sprite_manager):
        super().__init__(position, 'enemy', sprite_manager, 2, scale=2, drawing_rotation=-90)

        self.hitbox_radius = 50
        self.rotation = 0

        self.health_bar = HealthBar(self.position + pg.Vector2(0, 20), sprite_manager)

        self.velocity = pg.Vector2()
        self.acceleration = 1000
        self.max_speed = 800

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
        sound_manager = args[4]
        sprite_manager = args[5]

        super().update(dt)

        if not self.dead:
            # self.in_pursuit = False
            # update health bar position
            self.health_bar.position = self.position + pg.Vector2(0, 50)

            # update enemy state depending on health
            if self.health_bar.depleted:
                self.dead = True

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

            if distance_to_player > 300 and self.in_pursuit:
                rotation = random.randint(-100, 100) + self.rotation

                additional_velocity = pg.Vector2()

                additional_velocity.x += cos(radians(rotation)) * self.acceleration * dt
                additional_velocity.y -= sin(radians(rotation)) * self.acceleration * dt

                additional_velocity.clamp_magnitude(max(0, (self.max_speed // 2) - self.velocity.magnitude()))

                self.velocity += additional_velocity
            else:
                self.velocity /= 1.05

            self.velocity = self.velocity.clamp_magnitude(self.max_speed)

            self.position[0] += self.velocity.x * dt
            self.position[1] += self.velocity.y * dt

            # spawning lasers
            if distance_to_player < 500 and self.laser_cooldown < 0 and self.in_pursuit:
                self.spawn_laser = True
                self.laser_cooldown = self.cd + random.randint(0, 1000)/1000
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

                sound_manager.play('explosion')

                self.playing_animation = True
                self.rotation = 0
                super().__init__(self.position, 'explosion', sprite_manager, 5, scale=2)

            if self.animation_end:
                self.really_dead_and_should_be_destroyed = True


    def draw(self, *args):
        surf = args[0]
        scroll = args[1]
        time = args[2]
        if self.in_pursuit:
            self.health_bar.draw(surf, scroll)
        super().draw(surf, scroll, offset=(cos(time), sin(time)))
