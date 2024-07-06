import pygame as pg

WIDTH, HEIGHT = 1000, 800

BLANK = pg.Surface((1, 1))
BLANK.fill((128, 128, 128, 128))

FPS = 1000

# colors
BLACK = (13, 0, 26)
YELLOW = (242, 236, 139)
ORANGE = (251, 185, 84)
RED = (153, 61, 65)

# scene names
MAIN_MENU = 'main menu'
SETTINGS = 'settings'
MAIN_GAME = 'game'

default_font = pg.font.Font('assets/fonts/VCR_OSD_MONO_1.001.ttf', 40)
