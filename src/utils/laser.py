from src.utils.texture import Animation


class Laser(Animation):
    def __init__(self, position, type, speed, power):
        super().__init__(position, 'assets/textures/spritesheets/laser.png', (32, 32))
        self.type = type
        self.speed = speed
        self.power = power

        self.lifetime = 10  # seconds

    def draw(self, *args):
        surf = args[0]
        scroll = args[1]
        rotation = args[2]
        scale = args[3]
        super().draw(surf, scroll, rotation, scale)

    def update(self, *args):
