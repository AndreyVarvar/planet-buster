import pygame as pg

WIDTH, HEIGHT = 1000, 800

BLANK = pg.Surface((1, 1))
BLANK.fill((128, 128, 128, 128))

FPS = 100

# colors
BLACK = (13, 0, 26)

# scene names
MAIN_MENU = 'main menu'
SETTINGS = 'settings'
MAIN_GAME = 'game'

pixel_sans_font = pg.font.Font('assets/fonts/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf', 40)

# sounds
explosion = [pg.mixer.Sound('assets/sfx/explosion.wav'), pg.mixer.Sound('assets/sfx/explosion1.wav'), pg.mixer.Sound('assets/sfx/explosion2.wav')]


# settings
SFX_VOLUME = 1
MUSIC_VOLUME = 1
