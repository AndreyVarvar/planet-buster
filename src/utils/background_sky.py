from src.utils.constants import *
import random


class BackGroundSky:
    # parallax background of space filled with stars
    def __init__(self):
        self.sky = pg.image.load('assets/textures/sprites/star_sky.png')
        self.position = pg.Vector2(0, 0)

        self.width = WIDTH//self.sky.width
        self.height = HEIGHT//self.sky.height

    def draw(self, surf: pg.Surface):
        pos = pg.Vector2()
        pos.x = (self.position.x/10) % self.sky.width
        pos.y = (self.position.y/10) % self.sky.height

        self.position.x = self.position.x % 10_000
        self.position.y = self.position.y % 10_000

        for x in range(-1, self.width):
            for y in range(-1, self.height):
                surf.blit(self.sky, (pos.x+self.sky.width*x, pos.y+self.sky.height*y))
