# synonym of the work 'object' to not conflict with bild int keyword object in python
import pygame as pg
from src.utils.constants import WIDTH, HEIGHT


class Thingy:
    def __init__(self, position=pg.Vector2(0, 0), texture=pg.Surface((10, 10))):
        self.position = pg.Vector2(position)
        self.texture = texture

    def draw(self, surf, scroll, rotation=0, scale=1):

        texture = pg.transform.scale_by(self.texture, scale)
        texture = pg.transform.rotate(texture, rotation)

        pos = texture.get_rect(center=self.position)

        pos.x -= scroll[0] - WIDTH // 2
        pos.y -= scroll[1] - HEIGHT // 2

        surf.blit(texture, pos)
