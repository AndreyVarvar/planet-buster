from src.utils.scene_manager import scene_manager
from src.utils.scene import Scene
from src.utils.constants import *

from src.UI.button import Button
from src.UI.slider import Slider

from src.utils.texture import Texture
from math import cos, sin


button_outline = pg.image.load('assets/textures/UI/button_outline.png')
button_outline_hovered = pg.image.load('assets/textures/UI/button_outline_hover.png')


# here lie short scenes, that do not require a lot of space
class MainMenu(Scene):
    def __init__(self, scene_manager):
        super().__init__(MAIN_MENU, scene_manager)

        self.time = 0

    def draw_scene(self, *args):
        surf = args[0]

        self.button1.draw(surf)
        self.button2.draw(surf)
        self.button3.draw(surf)

        self.logo.draw(surf, (0, 0), 0, 2)

    def update(self, *args):
        mouse_pos = args[0]
        cursor = args[1]
        dt = args[2]
        sound_manager = args[5]

        self.time += dt

        self.button1.update(mouse_pos, cursor, sound_manager)
        self.button2.update(mouse_pos, cursor, sound_manager)
        self.button3.update(mouse_pos, cursor, sound_manager)

        # self.logo.position.x += cos(self.time)/10
        self.logo.position.y += sin(self.time)/10

        if self.button1.pressed:
            self.change_scene = True
            self.change_to = MAIN_GAME

        if self.button2.pressed:
            self.change_scene = True
            self.change_to = SETTINGS

        if self.button3.pressed:
            self.change_scene = True
            self.change_to = 'quit'

    def scene_thingies_init(self, *args):
        self.button1 = Button((500, 400), (400, 80), text='play', font=pixel_sans_font, texture=button_outline, hover_texture=button_outline_hovered, text_color=ORANGE)
        self.button2 = Button((500, 500), (400, 80), text='settings', font=pixel_sans_font, texture=button_outline, hover_texture=button_outline_hovered, text_color=ORANGE)
        self.button3 = Button((500, 600), (400, 80), text='quit', font=pixel_sans_font, texture=button_outline, hover_texture=button_outline_hovered, text_color=RED)

        self.logo = Texture((0, -225), 'assets/textures/sprites/planet_buster_logo.png')


class Settings(Scene):
    def __init__(self, scene_manager):
        super().__init__(SETTINGS, scene_manager)

    def draw_scene(self, *args):
        surf = args[0]

        self.button1.draw(surf)

        self.slider1.draw(surf)
        self.slider2.draw(surf)

    def update(self, *args):
        global SFX_VOLUME, MUSIC_VOLUME  # I just had to

        mouse_pos = args[0]  # just for clarity
        cursor = args[1]
        sound_manager = args[5]

        self.button1.update(mouse_pos, cursor, sound_manager)

        self.slider1.update(mouse_pos, cursor, sound_manager)
        sound_manager.set_volume(self.slider1.value)

        self.slider2.update(mouse_pos, cursor, sound_manager)

        if self.button1.pressed:
            self.change_scene = True
            self.change_to = MAIN_MENU

    def scene_thingies_init(self, *args):
        self.button1 = Button((500, 100), (400, 80), text='back', font=pixel_sans_font, texture=button_outline, hover_texture=button_outline_hovered, text_color=ORANGE)

        self.slider1 = Slider((500, 300), (400, 30), (50, 50), 0, 1, 0.3, 0.1, 'sfx volume')
        self.slider2 = Slider((500, 450), (400, 30), (50, 50), 0, 1, 1, 0.1, 'music volume')


MainMenu(scene_manager)  # initializing for it to be added to the scene_manager list
Settings(scene_manager)

