from src.utils.game_files.planet import CelestialBody
from math import *
import random


def generate_map(sprite_manager, difficulty):
    planets = []
    if difficulty < 8:
        planets.append(CelestialBody((0, 0), 'sun', difficulty % 4, sprite_manager))  # the SUN
    else:
        planets.append(CelestialBody((0, 0), 'black hole', -1, sprite_manager))  # the SUN

    # depending on difficulty add more planets
    planet_count = random.randint(10, min(15, 10+difficulty))
    for i in range(planet_count):
        random_rotation = radians(random.randint(0, 360))
        distance_from_center = (i+1)*(10_000/(planet_count+1))
        planet_pos = (distance_from_center*cos(random_rotation), distance_from_center*sin(random_rotation))
        planets.append(CelestialBody(planet_pos, 'planet', -1, sprite_manager))  # the SUN

    return planets
