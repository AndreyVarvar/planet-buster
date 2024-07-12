from src.utils.game_files.enemy import Enemy
from math import *
from src.utils.constants import *
import random


class EnemySpawnManager:
    def __init__(self, difficulty):
        self.next_wave_in = 0
        self.wave_count = 0

        self.difficulty = difficulty

    def update(self, dt, scroll, sprite_manager):
        self.next_wave_in -= dt

        if self.next_wave_in <= 0:
            self.wave_count += 1
            self.next_wave_in = sqrt(self.wave_count + 10) + 2 - floor(self.difficulty/10)

            enemy_count = ceil(sqrt(self.wave_count)/2) + floor(self.difficulty/5)

            enemies = set()
            for i in range(enemy_count):
                rotation = radians(random.randint(0, 360))
                enemy_pos = pg.Vector2(scroll) + pg.Vector2(cos(rotation)*WIDTH, sin(rotation)*HEIGHT)
                enemy = Enemy(enemy_pos, sprite_manager)
                enemy.in_pursuit = True
                enemies.add(enemy)

            return enemies

        return set()

