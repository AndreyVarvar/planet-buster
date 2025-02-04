from src.utils.animation import Animation
import random
from math import sqrt, atan2, degrees, cos, sin, radians
import pygame as pg


class CelestialBody(Animation):
    def __init__(self, position, type, i, sprite_manager, distance_from_center, revolution_angle, revolution_speed, scale=-1, target=False):
        paths = {
            "planet": ['assets/textures/spritesheets/planets/planet1.png',
                       'assets/textures/spritesheets/planets/planet2.png',
                       'assets/textures/spritesheets/planets/planet3.png',
                       'assets/textures/spritesheets/planets/planet4.png',
                       'assets/textures/spritesheets/planets/planet5.png',
                       'assets/textures/spritesheets/planets/planet6.png',
                       'assets/textures/spritesheets/planets/planet8.png',
                       'assets/textures/spritesheets/planets/planet9.png',
                       'assets/textures/spritesheets/planets/planet10.png',
                       'assets/textures/spritesheets/planets/planet101.png',
                       'assets/textures/spritesheets/planets/planet102.png',
                       'assets/textures/spritesheets/planets/planet103.png',
                       'assets/textures/spritesheets/planets/planet104.png',
                       'assets/textures/spritesheets/planets/planet105.png',
                       'assets/textures/spritesheets/planets/planet106.png',
                       'assets/textures/spritesheets/planets/planet107.png',
                       'assets/textures/spritesheets/planets/planet108.png',
                       'assets/textures/spritesheets/planets/planet109.png',
                       'assets/textures/spritesheets/planets/planet110.png'
                       ],

            "gas giant": ['assets/textures/spritesheets/planets/planet7.png',
                          'assets/textures/spritesheets/planets/planet111.png',
                          'assets/textures/spritesheets/planets/planet112.png',
                          'assets/textures/spritesheets/planets/planet113.png',
                          'assets/textures/spritesheets/planets/planet114.png',
                          'assets/textures/spritesheets/planets/planet115.png',],

            "sun": ['assets/textures/spritesheets/planets/sun1.png',
                    'assets/textures/spritesheets/planets/sun2.png',
                    'assets/textures/spritesheets/planets/sun3.png',
                    'assets/textures/spritesheets/planets/sun4.png'
                    ],

            "galaxy": ['assets/textures/spritesheets/planets/galaxy.png'],

            "black hole": ['assets/textures/spritesheets/planets/black_hole.png']
        }

        frame_dimensions = {
            "planet": (100, 100),
            "sun": (200, 200),
            "gas giant": (300, 300),
            "black hole": (200, 200),
            "galaxy": (100, 100)
        }

        fps = {
            "planet": 5,
            "sun": 2,
            "gas giant": 3,
            "black hole": 10,
            "galaxy": 5
        }

        scales = {
            "planet": [5, 20],  # random number in range of [a, b] (in range of a to b)
            "sun": [30, 50],
            "gas giant": [10, 25],
            "black hole": [50, 70],
            "galaxy": [10, 10]
        }

        path: str = paths[type][i] if i != -1 else random.choice(paths[type])

        name = path.split('/')[-1].split('.')[0]

        sprite_manager.add(name, path, True, frame_dimensions[type])

        super().__init__(position, name, sprite_manager, fps=fps[type])
        if scale != -1:
            self.scale = scale
        else:
            self.scale = random.randint(scales[type][0], scales[type][1]) / 10
        self.name = name

        density = {
            'planet': 1,
            "gas giant": 0.5,
            'sun': 2,
            'black hole': 3,
            'galaxy': 1
        }

        self.mass = (self.scale*100)**3 * density[type]

        self.radius = 50*self.scale

        self.type = type

        self.destroyed = False
        self.exploded = False
        self.done_exploding = False

        self.distance_from_center = distance_from_center
        self.revolution_angle = revolution_angle
        self.revolution_speed = revolution_speed

        self.target = target

    def update(self, *args):
        dt = args[0]
        sprite_manager = args[1]

        self.revolution_angle += self.revolution_speed*dt
        self.position.x = self.distance_from_center*cos(radians(self.revolution_angle))
        self.position.y = self.distance_from_center*sin(radians(self.revolution_angle))

        if self.destroyed and self.exploded is False:
            super().__init__(self.position, 'planet exploding', sprite_manager, 3, self.radius/32)
            self.exploded = True

        if self.animation_end and self.exploded:
            self.done_exploding = True

        super().update(dt)

    def draw(self, *args):
        surf = args[0]
        scroll = args[1]
        time = args[2]

        if not (self.exploded and self.animation_end):
            super().draw(surf, scroll, offset=(cos(time)*self.scale, sin(time)*self.scale))

    def apply_gravity(self, other_object, dt):
        distance = sqrt((other_object.position.x-self.position.x)**2 + (other_object.position.y-self.position.y)**2)

        if distance < 10_000:
            angle = degrees(atan2(-self.position.y+other_object.position.y, self.position.x-other_object.position.x))

            force = self.mass/(distance**2) * dt

            other_object.velocity.x += force*cos(radians(angle))
            other_object.velocity.y -= force*sin(radians(angle))

            if distance < (other_object.hitbox_radius + self.radius):
                other_object.dead = True
                other_object.health_bar.bar_state = 0
