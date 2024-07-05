from src.utils.constants import *
import random


class BackGroundSky:
    # parallax background of space filled with stars
    def __init__(self):
        self.sky = pg.image.load('assets/textures/sprites/star_sky.png')
        self.sky2 = pg.image.load('assets/textures/sprites/star_sky2.png')

        self.position = pg.Vector2(0, 0)

        self.width = WIDTH//self.sky.width
        self.height = HEIGHT//self.sky.height

        self.width2 = WIDTH//self.sky2.width
        self.height2 = HEIGHT//self.sky2.height

    def draw(self, surf: pg.Surface):
        self.position.x = self.position.x % 20_000
        self.position.y = self.position.y % 20_000

        # the 'furthest' layer is drawn first
        pos1 = pg.Vector2()
        pos1.x = (self.position.x/20) % self.sky.width
        pos1.y = (self.position.y/20) % self.sky.height

        for x in range(-1, self.width):
            for y in range(-1, self.height):
                surf.blit(self.sky, (pos1.x+self.sky.width*x, pos1.y+self.sky.height*y))

        # then the closer one
        pos2 = pg.Vector2()
        pos2.x = (self.position.x/10) % self.sky2.width
        pos2.y = (self.position.y/10) % self.sky2.height

        for x in range(-1, self.width2):
            for y in range(-1, self.height2):
                surf.blit(self.sky2, (pos2.x+self.sky2.width*x, pos2.y+self.sky2.height*y))
