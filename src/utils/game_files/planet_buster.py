from src.utils.thingy import Thingy
from math import *


class PlanetBuster(Thingy):
    def __init__(self, position, sprite_manager):
        super().__init__(position, sprite_manager.sprites['planet buster'], drawing_angle_offset=-90, scale=1.5)
        self.target = None
        self.exploded = False
        self.velocity = 200

    def update(self, dt):

        self.rotation = degrees(atan2(-self.position.y + self.target.position.y, self.position.x - self.target.position.x)) + 180
        self.position.x += self.velocity * dt * cos(radians(self.rotation))
        self.position.y -= self.velocity * dt * sin(radians(self.rotation))
