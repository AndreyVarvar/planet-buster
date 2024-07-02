from src.utils.scene_manager import scene_manager
from src.utils.scene import Scene
from src.utils.constants import *
from src.utils.texture import Texture, Animation
from math import atan2, degrees
from src.utils.player import Player
from src.utils.laser import Projectile
from src.utils.enemy import Enemy
from src.utils.planet import CelestialBody
# here lies the massive scene that is out game


class MainGame(Scene):
    def __init__(self, scene_manager):
        super().__init__(MAIN_GAME, scene_manager)

        self.projectiles = []

    def draw_scene(self, *args):
        surf = args[0]
        scroll = args[2]
        surf.fill(BLACK)

        for planet in self.planets:
            planet.draw(surf, scroll)

        for projectile in self.projectiles:
            projectile.draw(surf, scroll)

        for enemy in self.enemies:
            enemy.draw(surf, scroll)

        self.player.draw(surf, scroll)

    def update(self, *args):
        mouse_pos = args[0]
        cursor = args[1]
        dt = args[2]
        scroll = args[3]
        keys_pressed = args[4]

        # update every planet
        for planet in self.planets:
            planet.update(dt)

            # as well as apply gravity
            planet.apply_gravity(self.player, dt)

            for enemy in self.enemies:
                planet.apply_gravity(enemy, dt)

        # update the player
        self.player.update(dt, mouse_pos, scroll, keys_pressed, cursor)

        # update projectiles
        for projectile in self.projectiles.copy():
            projectile.update(dt)

            if projectile.self_destruct:
                self.projectiles.remove(projectile)

        # update enemies
        for enemy in self.enemies:
            enemy.update(dt, self.player.position)

            if enemy.spawn_laser:  # spawn lasers
                self.projectiles.append(Projectile(enemy.position, 2, 1000, 20, 180+degrees(atan2(-enemy.position.y+self.player.position.y, enemy.position.x-self.player.position.x))))

        # spawn lasers
        if self.player.spawn_laser:
            self.projectiles.append(Projectile(self.player.position, 0, 1000, 100, degrees(atan2(self.player.position.y-mouse_pos[1]-scroll[1]+HEIGHT//2, -self.player.position.x+mouse_pos[0]+scroll[0]-WIDTH//2))))

    def scene_thingies_init(self, *args):
        self.planets = []
        self.planets.append(CelestialBody((0, 0), 'sun', 0))
        self.planets.append(CelestialBody((1000, 1000), 'planet', 0))
        self.planets.append(CelestialBody((0, 1000), 'planet', 1))
        self.planets.append(CelestialBody((-1000, 1000), 'planet', 2))
        self.planets.append(CelestialBody((1000, 0), 'planet', 3))


        self.player = Player((300, 0))

        self.enemies = [Enemy((-100, -100)), Enemy((-100, 100)), Enemy((-100, 0))]


MainGame(scene_manager)
