from src.utils.texture import Animation
from math import cos, sin, radians


class Projectile(Animation):
    def __init__(self, position, type, speed, power, rotation, scale=1):
        super().__init__(position, 'assets/textures/spritesheets/laser.png', (32, 32))
        self.texture = self.animation[type]

        self.type = type
        self.speed = speed
        self.power = power
        self.rotation = rotation

        self.scale = scale

        self.lifetime = 10  # seconds

        self.spawn_timer = 0

        self.self_destruct = False

    def draw(self, *args):
        surf = args[0]
        scroll = args[1]

        super().draw(surf, scroll, self.rotation-90, self.scale)

    def update(self, *args):
        dt = args[0]

        self.spawn_timer += dt

        self.position.x += cos(radians(self.rotation)) * self.speed * dt
        self.position.y -= sin(radians(self.rotation)) * self.speed * dt

        if self.spawn_timer > self.lifetime:
            self.self_destruct = True