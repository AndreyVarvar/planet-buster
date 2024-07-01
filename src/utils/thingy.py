# synonym of the work 'object' to not conflict with bild int keyword object in python
import pygame as pg


class Thingy:
    def __init__(self, position=pg.Vector2(0, 0), texture=pg.Surface((10, 10))):
        self.position = position
        self.texture = texture

    def draw(self, surf):
        surf.blit(self.texture, self.position)
