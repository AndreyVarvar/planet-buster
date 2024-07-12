from src.utils.animation import Animation
from math import sin, cos, radians, floor
from src.utils.constants import *
from src.utils.game_files.healthbar import HealthBar
import random


class Player(Animation):
    def __init__(self, position, sprite_manager):
        super().__init__(position, 'player', sprite_manager, 2, scale=2, drawing_rotation=-90)

        # player stats
        self.hitbox_radius = 25
        self.rotation = 0

        self.health_bar = HealthBar(self.position+pg.Vector2(0, 20), sprite_manager)

        self.velocity = pg.Vector2()
        self.acceleration = 500
        self.max_speed = 700

        self.dead = False
        self.exploded = False
        self.really_dead = False

        self.angular_velocity = 180  # degrees per sec

        # laser spawning stuff
        self.laser_cooldown = 0
        self.cd = 0.2
        self.spawn_laser = False
        self.target_locked = False
        self.target = None

        # planet buster stuff
        self.fire_planet_buster = False
        self.used_the_only_attempt = False
        self.planet_buster_activated = False
        self.planet_buster_activation_time = 15  # seconds

    def update(self, *args):
        dt = args[0]
        mouse_pos = args[1]
        scroll = args[2]
        keys_pressed = args[3]
        cursor = args[4]
        map_boundaries = args[5]
        sound_manager = args[6]
        sprite_manager = args[7]
        crosshair = args[8]

        super().update(dt)

        if not self.dead:
            # update health bar position
            self.health_bar.position = self.position + pg.Vector2(0, 50)

            # update player state depending on health
            if self.health_bar.depleted is True:
                self.dead = True

            self.update_position_and_velocity(dt, keys_pressed)
            self.spawn_lasers(dt, cursor)

            self.dont_go_out_of_bounds(map_boundaries)
            self.dont_make_scroll_go_out_of_bounds(scroll, map_boundaries)

            self.update_scroll(scroll, mouse_pos)

            self.PLANET_BUSTER(keys_pressed, crosshair, dt)
        else:
            if not self.exploded:
                scroll[0] += random.randint(-100, 100)
                scroll[1] += random.randint(-100, 100)

                self.health_bar.bar_state = 0
                sound_manager.play('explosion')

                self.exploded = True
                self.rotation = 90
                super().__init__(self.position, 'explosion', sprite_manager, 3, scale=2)

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

    def update_position_and_velocity(self, dt, keys_pressed):
        # updating the rotation
        if keys_pressed[pg.K_a]:
            self.rotation += self.angular_velocity * dt

        if keys_pressed[pg.K_d]:
            self.rotation -= self.angular_velocity * dt

        # updating the position
        if keys_pressed[pg.K_w]:
            additional_velocity = pg.Vector2()

            additional_velocity.x += cos(radians(self.rotation)) * self.acceleration * dt
            additional_velocity.y -= sin(radians(self.rotation)) * self.acceleration * dt

            additional_velocity.clamp_magnitude(max(0, (self.max_speed // 2) - self.velocity.magnitude()))

            self.velocity += additional_velocity

        if keys_pressed[pg.K_s]:
            self.velocity /= 1.1

        self.velocity = self.velocity.clamp_magnitude(self.max_speed)

        self.position[0] += self.velocity.x * dt
        self.position[1] += self.velocity.y * dt

    def dont_make_scroll_go_out_of_bounds(self, scroll, map_boundaries):
        # make sure scroll also doesn't go out of bounds:
        if (scroll[1] - HEIGHT // 2) < map_boundaries.top:
            scroll[1] = map_boundaries.top + HEIGHT // 2
        elif (scroll[1] + HEIGHT // 2) > map_boundaries.bottom:
            scroll[1] = map_boundaries.bottom - HEIGHT // 2

        if (scroll[0] - WIDTH // 2) < map_boundaries.left:
            scroll[0] = map_boundaries.left + WIDTH // 2
        elif (scroll[0] + WIDTH // 2) > map_boundaries.right:
            scroll[0] = map_boundaries.right - WIDTH // 2

    def dont_go_out_of_bounds(self, map_boundaries):
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

    def spawn_lasers(self, dt, cursor):
        # spawning lasers
        if cursor.holding and self.laser_cooldown < 0:
            self.spawn_laser = True
            self.laser_cooldown = self.cd
        else:
            self.spawn_laser = False
            self.laser_cooldown -= dt

    def update_scroll(self, scroll, mouse_pos):
        # update scroll
        new_scroll = self.position.lerp(pg.Vector2(scroll) + pg.Vector2(mouse_pos) - pg.Vector2(WIDTH // 2, HEIGHT // 2), 0.2)
        scroll[0] = (new_scroll[0] + scroll[0]) / 2
        scroll[1] = (new_scroll[1] + scroll[1]) / 2

    def PLANET_BUSTER(self, keys_pressed, crosshair, dt):
        if crosshair.locked_on == 'planet' and self.used_the_only_attempt is False:
            if keys_pressed[pg.K_SPACE]:
                self.planet_buster_activated = True

        if self.planet_buster_activated:
            self.planet_buster_activation_time -= dt

            if self.planet_buster_activation_time <= 0:
                self.fire_planet_buster = True
