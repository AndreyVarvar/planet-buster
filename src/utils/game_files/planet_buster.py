from src.utils.thingy import Thingy
from math import *


class PlanetBuster(Thingy):
    def __init__(self, position, sprite_manager):
        super().__init__(position, sprite_manager.sprites['planet buster'], drawing_angle_offset=-90, scale=1.5)
        self.target = None
        self.exploded = False
        self.velocity = 0
        self.acceleration = 200
        self.max_velocity = 400

    def update(self, dt):

        self.velocity += self.acceleration*dt
        self.velocity = min(self.velocity, self.max_velocity)

        self.rotation = 180 + degrees(atan2(-self.position.y + self.target.position.y, self.position.x - self.target.position.x))
        self.position.x += self.velocity * dt * cos(self.rotation)
        self.position.y -= self.velocity * dt * sin(self.rotation)
