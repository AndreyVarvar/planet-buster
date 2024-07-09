from src.utils.thingy import Thingy
from math import cos, dist
from src.utils.constants import *


class CrossHair(Thingy):
    def __init__(self, position, sprite_manager):
        super().__init__(position, pg.transform.scale_by(sprite_manager.sprites['crosshair'], 1))

        self.locked_on = 'None'
        self.time = 0

    def update(self, dt, player, enemies, planets, mouse_pos, scroll, sprite_manager):
        mouse_pos_in_world = pg.Vector2(mouse_pos) + pg.Vector2(scroll) - pg.Vector2(WIDTH // 2, HEIGHT // 2)

        # find the closest enemy
        closest_enemy = None
        if len(enemies) > 0:
            closest_enemy = enemies[0]
            for enemy in enemies:
                if dist(mouse_pos_in_world, enemy.position) < dist(mouse_pos_in_world, closest_enemy.position) and enemy.dead is False:
                    closest_enemy = enemy

        # find the closest planet
        closest_planet = planets[1]
        for planet in planets[1:]:
            if dist(mouse_pos_in_world, planet.position) < dist(mouse_pos_in_world, closest_planet.position):
                closest_planet = planet

        # choose to aim for the planet or the enemy
        if closest_enemy is not None and dist(mouse_pos_in_world, closest_enemy.position) < 100 and player.dead is False:
            player.target_locked = True
            player.target = closest_enemy
            self.position = closest_enemy.position
            self.locked_on = 'enemy'
        elif dist(mouse_pos_in_world, closest_planet.position) < closest_planet.radius:
            player.target_locked = True
            player.target = closest_planet
            self.position = closest_planet.position
            self.locked_on = 'planet'
        else:
            player.target_locked = False
            player.target = None
            self.position = (-100, -100)
            self.locked_on = 'None'



        self.time += dt*40

        scale = (cos(self.time/10)/4+2)*(2 if self.locked_on in ['planet', 'gas giant'] else 1)
        self.texture = pg.transform.rotate(pg.transform.scale_by(sprite_manager.sprites['crosshair'], scale), self.time)

