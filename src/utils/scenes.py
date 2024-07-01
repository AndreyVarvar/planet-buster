from src.utils.scene_manager import scene_manager
from src.utils.scene import Scene
from src.utils.constants import *
from src.UI.button import Button

# here lie short scenes, that do not require a lot of space
class MainMenu(Scene):
    def __init__(self, scene_manager):
        super().__init__(MAIN_MENU, scene_manager)

    def draw_scene(self, *args):
        surf = args[0]

        surf.fill(BLACK)

        self.button1.draw(surf)
        self.button2.draw(surf)

    def update(self, *args):
        self.button1.update(*args)
        self.button2.update(*args)

        if self.button1.pressed:
            self.change_scene = True
            self.change_to = MAIN_GAME

        if self.button2.pressed:
            self.change_scene = True
            self.change_to = SETTINGS

    def scene_thingies_init(self, *args):
        self.button1 = Button((500, 200), (400, 80), text='play')
        self.button2 = Button((500, 300), (400, 80), text='settings')


class Settings(Scene):
    def __init__(self, scene_manager):
        super().__init__(SETTINGS, scene_manager)

    def draw_scene(self, *args):
        surf = args[0]

        surf.fill(BLACK)

        self.button1.draw(surf)
        self.button2.draw(surf)

    def update(self, *args):
        self.button1.update(*args)
        self.button2.update(*args)

        if self.button1.pressed:
            self.change_scene = True
            self.change_to = MAIN_MENU

    def scene_thingies_init(self, *args):
        self.button1 = Button((100, 100), (100, 80), text='back')
        self.button2 = Button((500, 300), (400, 80), text='HAHHAHHAHA')



MainMenu(scene_manager)  # initializing for it to be added to the scene_manager list
Settings(scene_manager)

