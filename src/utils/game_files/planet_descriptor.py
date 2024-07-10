from src.utils.thingy import Thingy
import pygame as pg
from src.utils.constants import WIDTH, HEIGHT


class Descriptor(Thingy):
    def __init__(self, position, sprite_manager, target):
        super().__init__(position, sprite_manager.sprites['planet descriptor'], scale=3)
        planet_image = pg.transform.scale(target.texture, (40, 40))
        pos = planet_image.get_rect(center=(32, 32))

        self.texture.blit(planet_image, pos)
        self.target = target
