from src.utils.scene_manager import scene_manager
from src.utils.scene import Scene
from src.utils.constants import *
from src.utils.texture import Texture, Animation
from math import atan2, degrees
from src.utils.player import Player
from src.utils.laser import Projectile
from src.utils.enemy import Enemy
from src.utils.planet import CelestialBody
from src.utils.utilities import render_text_with_shadow
# here lies the massive scene that is out game


class MainGame(Scene):
    def __init__(self):
        self.map_boundaries = pg.Rect(-10_000, -10_000, 20_000, 20_000)

        self.time = 0

        self.reset()

    def draw_scene(self, *args):
        surf = args[0]
        scroll = args[2]

        for planet in self.planets:
            planet.draw(surf, scroll, self.time)

        for projectile in self.projectiles:
            projectile.draw(surf, scroll)

        for enemy in self.enemies:
            enemy.draw(surf, scroll, self.time)

        self.player.draw(surf, scroll, self.time)

        surf.blit(render_text_with_shadow(2, f'[{round(self.player.position.x/10)}, {round(self.player.position.y/10)}]'), (10, 10))

    def update(self, *args):
        mouse_pos = args[0]
        cursor = args[1]
        dt = args[2]
        scroll = args[3]
        keys_pressed = args[4]
        sound_manager = args[5]
        background = args[6]

        self.time += dt

        # update the background according to the scroll
        background.position = -pg.Vector2(scroll)

        # update every planet
        for planet in self.planets:
            planet.update(dt)

            # as well as apply gravity
            planet.apply_gravity(self.player, dt)

            for enemy in self.enemies:
                planet.apply_gravity(enemy, dt)

        # update the player
        self.player.update(dt, mouse_pos, scroll, keys_pressed, cursor, self.map_boundaries, sound_manager)

        # update projectiles
        for projectile in self.projectiles.copy():
            projectile.update(dt)

            if projectile.self_destruct:
                self.projectiles.remove(projectile)

        # update enemies
        for enemy in self.enemies.copy():
            enemy.update(dt, self.player.position, self.map_boundaries, scroll, sound_manager)

            if enemy.spawn_laser:  # spawn lasers
                self.projectiles.append(Projectile(enemy.position, 2, 1000, 20, 180+degrees(atan2(-enemy.position.y+self.player.position.y, enemy.position.x-self.player.position.x)), sound_manager))

            if enemy.really_dead_and_should_be_destroyed:
                self.enemies.remove(enemy)
        # spawn lasers
        if self.player.spawn_laser:
            self.projectiles.append(Projectile(self.player.position, 0, 1000, 100, degrees(atan2(self.player.position.y-mouse_pos[1]-scroll[1]+HEIGHT//2, -self.player.position.x+mouse_pos[0]+scroll[0]-WIDTH//2)), sound_manager))

        # end game when player dies
        if self.player.really_dead:
            self.change_scene = True
            self.change_to = MAIN_MENU

    def scene_thingies_init(self, *args):
        self.planets = []
        self.planets.append(CelestialBody((0, 0), 'sun', -1))
        self.planets.append(CelestialBody((1000, 1000), 'planet', -1))
        self.planets.append(CelestialBody((0, 1000), 'planet', -1))
        self.planets.append(CelestialBody((-1000, 1000), 'planet', -1))
        self.planets.append(CelestialBody((1000, 0), 'planet', -1))


        self.player = Player((400, 0))

        self.enemies = [Enemy((-100, -1000)), Enemy((0, -1000)), Enemy((100, -1000)), Enemy((-100, -1100)), Enemy((0, -1100)), Enemy((100, -1100))]

    def reset(self, *args):
        super().__init__(MAIN_GAME, scene_manager)

        self.projectiles = []

        self.game_end = False


MainGame()
