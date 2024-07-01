from src.utils.scene_manager import scene_manager
from src.utils.scene import Scene
from src.utils.constants import *
from src.utils.texture import Texture, Animation
from math import atan2, pi
# here lies the massive scene that is out game


class MainGame(Scene):
    def __init__(self, scene_manager):
        super().__init__(MAIN_GAME, scene_manager)

    def draw_scene(self, *args):
        surf = args[0]
        scroll = args[2]
        mouse_pos = args[3]
        surf.fill(BLACK)

        self.sun.draw(surf, scroll, scale=10)
        player_angle = -90 + 180/pi*(-atan2(mouse_pos[1]+scroll[1]-HEIGHT//2, mouse_pos[0]+scroll[0]-WIDTH//2) + atan2(self.player.position[1], self.player.position[0]))
        if player_angle < 0:
            player_angle += 2*pi

        self.player.draw(surf, scroll, scale=2, rotation=player_angle)

    def update(self, *args):
        dt = args[2]

        self.sun.update(dt)
        self.player.update(dt)

    def scene_thingies_init(self, *args):
        self.sun = Animation((0, 0), 'assets/textures/spritesheets/HERECOMESTHESUN.png', (200, 200), 5)
        self.player = Animation((0, 0), 'assets/textures/spritesheets/spaceship.png', (32, 32), 2)

MainGame(scene_manager)
