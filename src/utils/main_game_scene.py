from src.utils.scene_manager import scene_manager
from src.utils.scene import Scene
from src.utils.constants import *
from src.utils.texture import Texture, Animation
from math import atan2, pi
from src.utils.player import Player
# here lies the massive scene that is out game


class MainGame(Scene):
    def __init__(self, scene_manager):
        super().__init__(MAIN_GAME, scene_manager)

    def draw_scene(self, *args):
        surf = args[0]
        scroll = args[2]
        surf.fill(BLACK)

        self.sun.draw(surf, scroll, scale=10)
        self.player.draw(surf, scroll)

    def update(self, *args):
        mouse_pos = args[0]
        dt = args[2]
        scroll = args[3]
        keys_pressed = args[4]

        self.sun.update(dt)
        self.player.update(dt, mouse_pos, scroll, keys_pressed)

    def scene_thingies_init(self, *args):
        self.sun = Animation((0, 0), 'assets/textures/spritesheets/HERECOMESTHESUN.png', (200, 200), 5)
        self.player = Player((0, 0))

MainGame(scene_manager)
