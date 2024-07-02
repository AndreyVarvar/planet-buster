from src.utils.scene_manager import scene_manager
from src.utils.scene import Scene
from src.utils.constants import *
from src.utils.texture import Texture, Animation
from math import atan2, degrees
from src.utils.player import Player
from src.utils.laser import Projectile
from src.utils.enemy import Enemy
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

        for planet in self.planets:
            planet.update(dt)

        self.player.update(dt, mouse_pos, scroll, keys_pressed, cursor)

        for projectile in self.projectiles.copy():
            projectile.update(dt)

            if projectile.self_destruct:
                self.projectiles.remove(projectile)

        for enemy in self.enemies:
            enemy.update(dt, self.player.position)

            if enemy.spawn_laser:
                self.projectiles.append(Projectile(enemy.position, 2, 1000, 20, 180+degrees(atan2(-enemy.position.y+self.player.position.y, enemy.position.x-self.player.position.x))))

        if self.player.spawn_laser:
            self.projectiles.append(Projectile(self.player.position, 0, 1000, 100, degrees(atan2(self.player.position.y-mouse_pos[1]-scroll[1]+HEIGHT//2, -self.player.position.x+mouse_pos[0]+scroll[0]-WIDTH//2))))

    def scene_thingies_init(self, *args):
        self.planets = []
        self.planets.append(Animation((0, 0), 'assets/textures/spritesheets/HERECOMESTHESUN.png', (200, 200), 5, scale=5))
        self.planets.append(Animation((1000, 1000), 'assets/textures/spritesheets/planet1.png', (100, 100), 5, scale=1))
        self.planets.append(Animation((-1000, 0), 'assets/textures/spritesheets/planet2.png', (100, 100), 5, scale=2.2))
        self.planets.append(Animation((200, -1000), 'assets/textures/spritesheets/planet3.png', (100, 100), 5, scale=1.5))


        self.player = Player((300, 0))

        self.enemies = [Enemy((-100, -100)), Enemy((-100, 100)), Enemy((-100, 0))]


MainGame(scene_manager)
