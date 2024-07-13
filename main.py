import asyncio

import pygame as pg
pg.mixer.pre_init()
pg.init()

from src.utils.constants import WIDTH, HEIGHT

display = pg.display.set_mode((WIDTH, HEIGHT))

from src.play import Game

game = Game(display)  # 1000 by 600 is the display size
asyncio.run(game.run())

pg.quit()
quit()
