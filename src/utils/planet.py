from src.utils.animation import Animation
import random
from math import sqrt, atan2, degrees, cos, sin, radians


class CelestialBody(Animation):
    def __init__(self, position, type, i, sprite_manager):
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
            "planet": [5, 20],  # random number in range of [a, b] (in range of a to b)
            "sun": [30, 50],
            "black hole": [100, 120],
            "galaxy": [10, 10]
        }

        path: str = paths[type][i] if i != -1 else random.choice(paths[type])

        name = path.split('/')[-1].split('.')[0]
        if i == 6:
            sprite_manager.add(name, path, True, (300, 300))
        else:
            sprite_manager.add(name, path, True, frame_dimensions[type])

        super().__init__(position, name, sprite_manager, fps=fps[type])

        self.scale = random.randint(scales[type][0], scales[type][1]) / 10
        self.name = name

        density = {
            'planet': 1,
            'sun': 3,
            'black hole': 10,
            'galaxy': 1
        }

        self.mass = (self.scale*100)**3 * density[type]

        self.radius = 50*self.scale

        self.type = type

    def update(self, *args):
        dt = args[0]
        super().update(dt)

    def draw(self, *args):
        surf = args[0]
        scroll = args[1]
        time = args[2]

        super().draw(surf, scroll, offset=(cos(time)*self.scale, sin(time)*self.scale))

    def apply_gravity(self, other_object, dt):
        distance = sqrt((other_object.position.x-self.position.x)**2 + (other_object.position.y-self.position.y)**2)

        if distance < 1000:
            angle = degrees(atan2(-self.position.y+other_object.position.y, self.position.x-other_object.position.x))

            force = self.mass/(distance**2) * dt

            other_object.velocity.x += force*cos(radians(angle))
            other_object.velocity.y -= force*sin(radians(angle))

            if distance < (other_object.hitbox_radius + self.radius):
                if other_object.velocity.magnitude() > 350 or self.type != 'planet':
                    other_object.dead = True
                else:
                    other_object.position.x = self.position.x - (self.radius + other_object.hitbox_radius)*cos(radians(angle))
                    other_object.position.y = self.position.y + (self.radius + other_object.hitbox_radius)*sin(radians(angle))

                    # unexplained math
                    A = angle
                    B = degrees(atan2(other_object.velocity.y, other_object.velocity.x))

                    d = other_object.velocity.magnitude()*cos(radians(90 - B + A))
                    other_object.velocity.x = d * cos(radians(90 + A))
                    other_object.velocity.y = d * -sin(radians(90 + A))