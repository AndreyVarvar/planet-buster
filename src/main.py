from src.utils.constants import *

from src.utils.cursor import Cursor

# managers
from src.utils.sound_manager import SoundManager
from src.utils.music_manager import MusicManager
from src.utils.scene_manager import SceneManager  # crazy namings
from src.utils.sprite_manager import SpriteManager

# scenes
from src.utils.scenes import MainMenu, Settings
from src.utils.main_game_scene import MainGame

from src.utils.background_sky import BackGroundSky

import src.utils.scenes, src.utils.main_game_scene  # aren't supposed to be used in here, but need to be 'called'


class Game:
    def __init__(self, display):
        self.display = display
        self.running = True

        # settings up sound manager
        self.sound_manager = SoundManager()
        self.sound_manager.add('explosion', [pg.mixer.Sound('assets/sfx/explosion.wav'), pg.mixer.Sound('assets/sfx/explosion1.wav'), pg.mixer.Sound('assets/sfx/explosion2.wav')], 'multiple')
        self.sound_manager.add('ui-button-hover', pg.mixer.Sound('assets/sfx/button_hover.wav'))
        self.sound_manager.add('ui-button-click', pg.mixer.Sound('assets/sfx/button_pressed.wav'))
        self.sound_manager.add('ui-slider-slide', pg.mixer.Sound('assets/sfx/slider_slide.wav'))
        self.sound_manager.add('laser-fired', pg.mixer.Sound('assets/sfx/laser.wav'))
        self.sound_manager.add('hurt', pg.mixer.Sound('assets/sfx/hurt.wav'))
        self.sound_manager.add('planet explosion', pg.mixer.Sound('assets/sfx/planet_explosing.wav'))
        self.sound_manager.add('whoosh', pg.mixer.Sound('assets/sfx/whoosh.wav'))
        self.sound_manager.add('thrust', pg.mixer.Sound('assets/sfx/thrust.wav'))


        self.sound_manager.set_volume(0.33)

        # setting up music manager
        self.music_manager = MusicManager()
        self.music_manager.add('intro', 'assets/music/intro.wav')

        # setting up sprite manager
        self.sprite_manager = SpriteManager()

        self.sprite_manager.add('sky', 'assets/textures/sprites/star_sky.png')
        self.sprite_manager.add('sky2', 'assets/textures/sprites/star_sky2.png')

        # setting up the scene manager
        self.scene_manager = SceneManager()
        self.scene_manager.add_scene(MAIN_MENU, MainMenu)
        self.scene_manager.add_scene(SETTINGS, Settings)
        self.scene_manager.add_scene(MAIN_GAME, MainGame)

        self.scene_manager.current_scene = self.scene_manager.scenes[MAIN_MENU](self.sprite_manager)


        self.background = BackGroundSky(self.sprite_manager)

        self.scroll = [0, 0]

        self.clock = pg.time.Clock()

        self.difficulty = 0

        self.cursor = Cursor()

        self.dt = 0

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS)/1000

            events = pg.event.get()

            self.event_handling(events)  # handle events bruh
            self.update()
            self.draw()

    def event_handling(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False

    def draw(self):
        self.display.fill(BLACK)
        self.background.draw(self.display)

        self.scene_manager.draw_scene(self.display, self.dt, self.scroll, pg.mouse.get_pos())

        pg.display.update()

    def update(self):
        self.scene_manager.update(pg.mouse.get_pos(), self.cursor, self.dt, self.scroll, pg.key.get_pressed(), self.sound_manager, self.background, self.sprite_manager, self.music_manager)

        self.cursor.update(pg.mouse.get_pressed())

        if self.scene_manager.leaving:
            self.running = False
