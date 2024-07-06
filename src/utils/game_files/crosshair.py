from src.utils.thingy import Thingy
from math import cos
from src.utils.constants import *


class CrossHair(Thingy):
    def __init__(self, position, sprite_manager):
        super().__init__(position, pg.transform.scale_by(sprite_manager.sprites['crosshair'], 1))


        self.time = 0

    def update(self, dt, sprite_manager):
        self.time += dt*40

        self.texture = pg.transform.rotate(pg.transform.scale_by(sprite_manager.sprites['crosshair'], cos(self.time/10)/4+2), self.time)
