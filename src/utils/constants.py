import pygame as pg

WIDTH, HEIGHT = 1000, 800

BLANK = pg.Surface((1, 1))
BLANK.fill((128, 128, 128, 128))

FPS = 30

# colors
BLACK = (13, 0, 26)
YELLOW = (242, 236, 139)
ORANGE = (251, 185, 84)
DARK_ORANGE = (205, 104, 61)
RED = (153, 61, 65)
DARK_RED = (122, 48, 69)
GREEN = (151, 147, 58)
DARK_GREEN = (95, 109, 67)

# scene names
MAIN_MENU = 'main menu'
SETTINGS = 'settings'
MAIN_GAME = 'game'
MISSION_FAIL = 'mission fail'
MISSION_SUCCESS = 'mission success'

default_font = pg.font.Font('assets/fonts/VCR_OSD_MONO_1.001.ttf', 40)
large_font = pg.font.Font('assets/fonts/VCR_OSD_MONO_1.001.ttf', 60)
