from src.utils.texture import Animation
import random
from math import sqrt, atan2, degrees, cos, sin, radians


class CelestialBody(Animation):
    def __init__(self, position, type, i):
        paths = {
            "planet": ['assets/textures/spritesheets/planet1.png',
                       'assets/textures/spritesheets/planet2.png',
                       'assets/textures/spritesheets/planet3.png',
                       'assets/textures/spritesheets/planet4.png',
                       'assets/textures/spritesheets/planet5.png',
                       'assets/textures/spritesheets/planet6.png',
                       'assets/textures/spritesheets/planet7.png',
                       'assets/textures/spritesheets/planet8.png',
                       'assets/textures/spritesheets/planet9.png',
                       'assets/textures/spritesheets/planet10.png'
                       ],

            "sun": ['assets/textures/spritesheets/sun1.png',
                    'assets/textures/spritesheets/sun2.png',
                    'assets/textures/spritesheets/sun3.png',
                    'assets/textures/spritesheets/sun4.png'
                    ],

            "galaxy": ['assets/textures/spritesheets/galaxy.png'],

            "black hole": ['assets/textures/spritesheets/black_hole.png']
        }

        frame_dimensions = {
            "planet": (100, 100),
            "sun": (200, 200),
            "black hole": (200, 200),
            "galaxy": (100, 100)
        }

        fps = {
            "planet": 10,
            "sun": 2,
            "black_hole": 20,
            "galaxy": 5
        }

        scales = {
            "planet": [5, 20],
            "sun": [30, 50],
            "black hole": [100, 120],
            "galaxy": [10, 10]
        }

        scale = random.randint(scales[type][0], scales[type][1])/10

        path = paths[type][i] if i != -1 else random.choice(paths[type])

        super().__init__(position, path, frame_dimensions[type], fps[type], scale)

        self.mass = (scale*100)**3/100

        self.radius = 50*scale

        self.type = type

    def update(self, *args):
        dt = args[0]
        super().update(dt)

    def draw(self, *args):
        surf = args[0]
        scroll = args[1]

        super().draw(surf, scroll)

    def apply_gravity(self, other_object, dt):
        distance = sqrt((other_object.position.x-self.position.x)**2 + (other_object.position.y-self.position.y)**2)

        if distance < 1000:
            angle = degrees(atan2(-self.position.y+other_object.position.y, self.position.x-other_object.position.x))

            force = self.mass/(distance**2) * dt

            other_object.velocity.x += force*cos(radians(angle))
            other_object.velocity.y -= force*sin(radians(angle))

            if distance < (other_object.hitbox_radius + self.radius):
                other_object.dead = True
