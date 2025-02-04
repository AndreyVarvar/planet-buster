from src.utils.game_files.planet import CelestialBody
from math import *
from src.utils.game_files.planet_descriptor import Descriptor
import random


def generate_map(sprite_manager, difficulty):
    planets = set()
    if difficulty < 8:
        planets.add(CelestialBody((0, 0), 'sun', difficulty % 4, sprite_manager, 0, 0, 0))  # the SUN
    else:
        planets.add(CelestialBody((0, 0), 'black hole', -1, sprite_manager, 0, 0, 0))  # the SUN

    # depending on difficulty add more planets
    planet_count = 10
    target = random.randint(0, planet_count - 1)
    planet_description = None

    for i in range(planet_count):
        random_rotation = radians(random.randint(0, 360))
        distance_from_center = (i+1)*(10_000/(planet_count+1))
        planet_pos = (distance_from_center*cos(random_rotation), distance_from_center*sin(random_rotation))
        rotation_speed = random.randint(planet_count//(i+1), planet_count//(i+1) + 1)/10  # the farther away, the slower the planet
        scale = random.randint(i//10+1, i//5+1)

        planet_type = random.choice(['planet', 'gas giant'])

        planet = CelestialBody(planet_pos, planet_type, -1, sprite_manager, distance_from_center, degrees(random_rotation), rotation_speed, scale)

        if i == target:
            planet.target = True
            planet_description = Descriptor((0, 0), sprite_manager, planet)

        planets.add(planet)  # the SUN

    return planets, planet_description
