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
        self.position.x = (self.position.x/10) % self.sky.width
        self.position.y = (self.position.y/10) % self.sky.height

        for x in range(-1, self.width):
            for y in range(-1, self.height):
                surf.blit(self.sky, (self.position.x+self.sky.width*x, self.position.y+self.sky.height*y))
