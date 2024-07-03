import pygame as pg
pg.init()

from src.utils.constants import WIDTH, HEIGHT

display = pg.display.set_mode((WIDTH, HEIGHT))

from src.main import Game

game = Game(display)  # 1000 by 600 is the display size
game.run()
