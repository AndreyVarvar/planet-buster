from src.utils.constants import *
from src.UI.button import Button



class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def update(self, *args):
        self.current_scene.update(*args)

        if self.current_scene.change_scene:
            self.current_scene.change_scene = False
            new_scene = self.current_scene.change_to
            self.current_scene.change_to = None

            self.current_scene = self.scenes[new_scene]

    def draw_scene(self, *args):
        self.current_scene.draw_scene(*args)


scene_manager = SceneManager()

MAIN_MENU = 'main menu'
SETTINGS = 'settings'
MAIN_GAME = 'game'


class Scene:
    def __init__(self, name):
        self.name = name
        self.change_scene = False
        self.change_to = None  # what scene to change to

        self.scene_thingies_init()  # init all object in the scene

        scene_manager.scenes.update({name: self})

    def scene_thingies_init(self, *args):
        pass

    def draw_scene(self, *args):
        pass

    def update(self, *args):
        pass  # in here we need logic for switching scenes


class MainMenu(Scene):
    def __init__(self):
        super().__init__(MAIN_MENU)

    def draw_scene(self, *args):
        surf = args[0]

        surf.fill(BLACK)

        self.button1.draw(surf)
        self.button2.draw(surf)

    def update(self, *args):
        self.button1.update(*args)
        self.button2.update(*args)

        if self.button2.pressed:
            self.change_scene = True
            self.change_to = SETTINGS

    def scene_thingies_init(self, *args):
        self.button1 = Button((500, 200), (400, 80), text='play')
        self.button2 = Button((500, 300), (400, 80), text='settings')


class Settings(Scene):
    def __init__(self):
        super().__init__(SETTINGS)

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


class MainGame(Scene):
    def __init__(self):
        super().__init__(MAIN_GAME)

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



MainMenu()  # initializing for it to be added to the scene_manager list
Settings()
