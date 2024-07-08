from src.utils.scene import Scene
from src.utils.constants import *

from src.UI.button import Button
from src.UI.slider import Slider

from src.utils.thingy import Thingy

from math import cos, sin


# here lie short scenes, that do not require a lot of space
class MainMenu(Scene):
    def __init__(self, *args):
        super().__init__(MAIN_MENU, *args)

        self.time = 0

    def draw_scene(self, *args):
        surf = args[0]

        self.button1.draw(surf)
        self.button2.draw(surf)
        self.button3.draw(surf)

        self.logo.draw(surf, (0, 0), (0, sin(self.time)))

    def update(self, *args):
        mouse_pos = args[0]
        cursor = args[1]
        dt = args[2]
        sound_manager = args[5]
        background = args[6]
        music_manager = args[8]

        self.time += dt

        music_manager.play('intro')

        background.position = pg.Vector2(background.position.x, background.position.y + 200*dt)

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
        sprite_manager = args[0]

        sprite_manager.add('button outline', 'assets/textures/UI/button_outline.png')
        sprite_manager.add('button outline on hover', 'assets/textures/UI/button_outline_hover.png')
        sprite_manager.add('logo', 'assets/textures/sprites/planet_buster_logo.png')

        button_outline = sprite_manager.sprites['button outline']
        button_outline_hovered = sprite_manager.sprites['button outline on hover']

        self.button1 = Button((500, 400), (400, 80), text='play', font=default_font, texture=button_outline, hover_texture=button_outline_hovered, text_color=ORANGE, text_with_shadow=True, shadow_color=RED)
        self.button2 = Button((500, 500), (400, 80), text='settings', font=default_font, texture=button_outline, hover_texture=button_outline_hovered, text_color=ORANGE, text_with_shadow=True, shadow_color=RED)
        self.button3 = Button((500, 600), (400, 80), text='quit', font=default_font, texture=button_outline, hover_texture=button_outline_hovered, text_color=RED, text_with_shadow=True, shadow_color=BLACK)

        self.logo = Thingy((0, -225), sprite_manager.sprites['logo'], scale=2)


class Settings(Scene):
    def __init__(self, *args):
        super().__init__(SETTINGS, *args)

    def draw_scene(self, *args):
        surf = args[0]

        self.button1.draw(surf)

        self.slider1.draw(surf)
        self.slider2.draw(surf)

    def update(self, *args):
        global SFX_VOLUME, MUSIC_VOLUME  # I just had to

        mouse_pos = args[0]  # just for clarity
        cursor = args[1]
        dt = args[2]
        sound_manager = args[5]
        background = args[6]
        music_manager = args[8]

        music_manager.play('intro')

        self.button1.update(mouse_pos, cursor, sound_manager)

        self.slider1.update(mouse_pos, cursor, sound_manager)
        sound_manager.set_volume(self.slider1.value)

        background.position = pg.Vector2(background.position.x, background.position.y + dt*100*(self.slider1.value*10 + 1))
        music_manager.set_volume(self.slider2.value)

        self.slider2.update(mouse_pos, cursor, sound_manager)

        if self.button1.pressed:
            self.change_scene = True
            self.change_to = MAIN_MENU

    def scene_thingies_init(self, *args):
        sprite_manager = args[0]
        sound_manager = args[1]
        music_manager = args[2]

        sprite_manager.add('button outline', 'assets/textures/UI/button_outline.png')
        sprite_manager.add('button outline on hover', 'assets/textures/UI/button_outline_hover.png')

        button_outline = sprite_manager.sprites['button outline']
        button_outline_hovered = sprite_manager.sprites['button outline on hover']

        self.button1 = Button((500, 100), (400, 80), text='back', font=default_font, texture=button_outline, hover_texture=button_outline_hovered, text_color=ORANGE, text_with_shadow=True, shadow_color=RED)

        self.slider1 = Slider((500, 300), (400, 30), (50, 50), 0, 1, sound_manager.volume, 0.05, 'sfx volume', desc_with_shadow=True, shadow_color=RED)
        self.slider2 = Slider((500, 450), (400, 30), (50, 50), 0, 1, music_manager.volume, 0.1, 'music volume', desc_with_shadow=True, shadow_color=RED)

