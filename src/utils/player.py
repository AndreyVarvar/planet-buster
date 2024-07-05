from src.utils.animation import Animation
import pygame as pg
from math import sin, cos, radians, floor
from src.utils.constants import *
from src.utils.healthbar import HealthBar
import random


class Player(Animation):
    def __init__(self, position, sprite_manager):
        super().__init__(position, 'player', sprite_manager, 2, scale=2, drawing_rotation=-90)

        self.hitbox_radius = 25
        self.rotation = 0

        self.health_bar = HealthBar(self.position+pg.Vector2(0, 20), sprite_manager)

        self.velocity = pg.Vector2()
        self.acceleration = 10
        self.max_speed = 700

        self.dead = False
        self.playing_animation = False
        self.really_dead = False

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
        map_boundaries = args[5]
        sound_manager = args[6]
        sprite_manager = args[7]

        super().update(dt)

        if not self.dead:
            # update health bar position
            self.health_bar.position = self.position + pg.Vector2(0, 50)

            # update player state depending on health
            if self.health_bar.depleted is True:
                self.dead = True

            # updating the rotation
            if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]:
                self.rotation += self.angular_velocity * dt

            if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]:
                self.rotation -= self.angular_velocity * dt

            # updating the position
            if keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]:
                additional_velocity = pg.Vector2()

                additional_velocity.x += cos(radians(self.rotation))*self.acceleration
                additional_velocity.y -= sin(radians(self.rotation))*self.acceleration

                additional_velocity.clamp_magnitude(max(0, (self.max_speed//2)-self.velocity.magnitude()))

                self.velocity += additional_velocity


            if keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s] or keys_pressed[pg.K_SPACE] or keys_pressed[pg.KMOD_SHIFT]:
                self.velocity /= 1.1

            self.velocity = self.velocity.clamp_magnitude(self.max_speed)

            self.position[0] += self.velocity.x * dt
            self.position[1] += self.velocity.y * dt

            # update scroll
            new_scroll = self.position.lerp(pg.Vector2(scroll)+pg.Vector2(mouse_pos)-pg.Vector2(WIDTH//2, HEIGHT//2), 0.2)
            scroll[0] = (new_scroll[0]+scroll[0])/2
            scroll[1] = (new_scroll[1]+scroll[1])/2


            # spawning lasers
            if cursor.holding and self.laser_cooldown < 0:
                self.spawn_laser = True
                self.laser_cooldown = self.cd
            else:
                self.spawn_laser = False
                self.laser_cooldown -= dt


            # make sure we don't leave out of bounds
            if (self.position.x - self.hitbox_radius) < map_boundaries.left:
                self.velocity.x = 0
                self.position.x = map_boundaries.left + self.hitbox_radius
            elif (self.position.x + self.hitbox_radius) > map_boundaries.right:
                self.velocity.x = 0
                self.position.x = map_boundaries.right - self.hitbox_radius

            if (self.position.y - self.hitbox_radius) < map_boundaries.top:
                self.velocity.y = 0
                self.position.y = map_boundaries.top + self.hitbox_radius
            elif (self.position.y + self.hitbox_radius) > map_boundaries.bottom:
                self.velocity.y = 0
                self.position.y = map_boundaries.bottom - self.hitbox_radius


            # make sure scroll also doesn't go out of bounds:
            if (scroll[1]-HEIGHT//2) < map_boundaries.top:
                scroll[1] = map_boundaries.top + HEIGHT//2
            elif (scroll[1]+HEIGHT//2) > map_boundaries.bottom:
                scroll[1] = map_boundaries.bottom - HEIGHT//2

            if (scroll[0]-WIDTH//2) < map_boundaries.left:
                scroll[0] = map_boundaries.left + WIDTH//2
            elif (scroll[0]+WIDTH//2) > map_boundaries.right:
                scroll[0] = map_boundaries.right - WIDTH//2
        else:
            if not self.playing_animation:
                scroll[0] += random.randint(-100, 100)
                scroll[1] += random.randint(-100, 100)

                self.health_bar.bar_state = 0
                sound_manager.play('explosion')

                self.playing_animation = True
                self.rotation = 90
                super().__init__(self.position, 'explosion', sprite_manager, 5, scale=2)

            scroll[0] += (-scroll[0]+self.position.x)/20
            scroll[1] += (-scroll[1]+self.position.y)/20

            scroll[0] = floor(scroll[0])
            scroll[1] = floor(scroll[1])

            if self.animation_end:
                self.really_dead = True


    def draw(self, *args):
        surf = args[0]
        scroll = args[1]
        time = args[2]

        self.health_bar.draw(surf, scroll)
        super().draw(surf, scroll, offset=(cos(time), sin(time)))
