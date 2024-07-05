# synonym of the work 'object' to not conflict with bild int keyword object in python
import pygame as pg
from src.utils.constants import WIDTH, HEIGHT
from math import cos, sin, floor


class Thingy:
    def __init__(self, position=pg.Vector2(0, 0), texture=pg.Surface((10, 10)), rotation=0, scale=1, drawing_angle_offset=0):
        self.position = pg.Vector2(position)
        self.texture = texture

        self.drawing_rotation = drawing_angle_offset
        self.rotation = rotation
        self.scale = scale

    def draw(self, surf, scroll, offset=pg.Vector2(0, 0)):

        texture = pg.transform.scale_by(self.texture, self.scale)
        texture = pg.transform.rotate(texture, self.rotation+self.drawing_rotation)

        pos = texture.get_rect(center=self.position)

        pos.x -= scroll[0] - WIDTH // 2
        pos.y -= scroll[1] - HEIGHT // 2

        pos.x += offset[0]
        pos.y += offset[1]

        pos.x = floor(pos.x)
        pos.y = floor(pos.y)

        surf.blit(texture, pos)
