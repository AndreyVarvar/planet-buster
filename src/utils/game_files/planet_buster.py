from src.utils.thingy import Thingy
from math import *


class PlanetBuster(Thingy):
    def __init__(self, position, sprite_manager):
        super().__init__(position, sprite_manager['planet buster'])
        self.target = None
        self.exploded = False
        self.velocity = 200

    def update(self, dt):
        if self.target is not None:
            self.rotation = 180 + degrees(atan2(-self.position.y + self.target.y, self.position.x - self.target.x))
            self.position.x += self.velocity * dt * cos(self.rotation)
            self.position.y -= self.velocity * dt * sin(self.rotation)
