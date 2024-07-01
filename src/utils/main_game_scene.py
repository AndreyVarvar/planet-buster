from src.utils.scene_manager import scene_manager
from src.utils.scene import Scene
from src.utils.constants import *
from src.utils.texture import Texture, Animation
from math import atan2, degrees
from src.utils.player import Player
from src.utils.laser import Projectile
# here lies the massive scene that is out game


class MainGame(Scene):
    def __init__(self, scene_manager):
        super().__init__(MAIN_GAME, scene_manager)

        self.projectiles = []

    def draw_scene(self, *args):
        surf = args[0]
        scroll = args[2]
        surf.fill(BLACK)

        self.sun.draw(surf, scroll, scale=5)

        for projectile in self.projectiles:
            projectile.draw(surf, scroll)

        self.player.draw(surf, scroll)

    def update(self, *args):
        mouse_pos = args[0]
        cursor = args[1]
        dt = args[2]
        scroll = args[3]
        keys_pressed = args[4]

        self.sun.update(dt)
        self.player.update(dt, mouse_pos, scroll, keys_pressed, cursor)

        for projectile in self.projectiles.copy():
            projectile.update(dt)

            if projectile.self_destruct:
                self.projectiles.remove(projectile)

        if self.player.spawn_laser:
            self.projectiles.append(Projectile(self.player.position, 0, 1000, 100, degrees(atan2(self.player.position.y-mouse_pos[1]-scroll[1]+HEIGHT//2, -self.player.position.x+mouse_pos[0]+scroll[0]-WIDTH//2))))

    def scene_thingies_init(self, *args):
        self.sun = Animation((0, 0), 'assets/textures/spritesheets/HERECOMESTHESUN.png', (200, 200), 5)
        self.player = Player((0, 0))


MainGame(scene_manager)
