from src.utils.thingy import Thingy
from math import *
import pygame as pg


class Radar(Thingy):
    def __init__(self, position, sprite_manager):
        self.load_markings(sprite_manager)

        super().__init__(position, sprite_manager.sprites['radar'], scale=4)

    def update(self, player, planets, enemies, sprite_manager):
        self.texture = sprite_manager.sprites['radar'].copy()

        # first draw all the planets on the radar
        for planet in planets:
            # get the correct mark
            if planet.type == 'sun':
                mark = sprite_manager.sprites['markings'][0]
            elif planet.type == 'black hole':
                mark = sprite_manager.sprites['markings'][1]
            elif planet.type == 'gas giant':
                mark = sprite_manager.sprites['markings'][2]
            elif planet.type == 'planet':
                mark = sprite_manager.sprites['markings'][3]

            # get the position of the mark on the radar
            mark_pos = ((planet.position - player.position)/80).clamp_magnitude(27) + pg.Vector2(29, 29)  # offset to the center of radar display
            self.texture.blit(mark, mark_pos)

        # second, we draw all the enemies on the radar
        for enemy in enemies:
            # get the correct mark
            mark = sprite_manager.sprites['markings'][5]

            # get the position of the mark on the radar
            mark_pos = ((enemy.position - player.position)/80).clamp_magnitude(27) + pg.Vector2(29, 29)  # offset to the center of radar display
            self.texture.blit(mark, mark_pos)

    @staticmethod
    def load_markings(sprite_manager):
        sprite_manager.add('radar', 'assets/textures/sprites/radar.png')
        sprite_manager.add('markings', 'assets/textures/sprites/radar_icons.png', True, (6, 6))
