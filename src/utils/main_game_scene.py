from src.utils.scene_manager import scene_manager
from src.utils.scene import Scene
from src.utils.constants import *

# here lies the massive scene that is out game


class MainGame(Scene):
    def __init__(self, scene_manager):
        super().__init__(MAIN_GAME, scene_manager)

    def draw_scene(self, *args):
        surf = args[0]

        surf.fill(BLACK)

    def update(self, *args):
        pass

    def scene_thingies_init(self, *args):
        pass


MainGame(scene_manager)
