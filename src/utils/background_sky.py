from src.utils.constants import *


class BackGroundSky:
    # parallax background of space filled with stars
    def __init__(self, sprite_manager):
        self.sky_fragment = sprite_manager.sprites['sky']
        self.sky2_fragment = sprite_manager.sprites['sky2']

        self.width = WIDTH // self.sky_fragment.get_width()
        self.height = HEIGHT // self.sky_fragment.get_height()

        self.width2 = WIDTH // self.sky2_fragment.get_width()
        self.height2 = HEIGHT // self.sky2_fragment.get_height()

        self.sky = pg.Surface((self.sky_fragment.get_width()*(self.width+1), self.sky_fragment.get_height()*(self.height+1)), pg.SRCALPHA)
        self.sky2 = pg.Surface((self.sky2_fragment.get_width()*(self.width2+1), self.sky2_fragment.get_height()*(self.height2+1)), pg.SRCALPHA)

        for x in range(self.width+1):
            for y in range(self.height+1):
                self.sky.blit(self.sky_fragment, (self.sky_fragment.get_width() * x, self.sky_fragment.get_height() * y))

        for x in range(self.width2+1):
            for y in range(self.height2+1):
                self.sky2.blit(self.sky2_fragment, (self.sky2_fragment.get_width() * x, self.sky2_fragment.get_height() * y))

        self.position = pg.Vector2(0, 0)

        self.sky = self.sky.convert_alpha()
        self.sky2 = self.sky2.convert_alpha()

    def draw(self, surf: pg.Surface):
        pos1 = pg.Vector2()
        pos1.x = (self.position.x / 20) % self.sky_fragment.get_width() - self.sky_fragment.get_width()
        pos1.y = (self.position.y / 20) % self.sky_fragment.get_height() - self.sky_fragment.get_height()

        pos2 = pg.Vector2()
        pos2.x = (self.position.x / 10) % self.sky2_fragment.get_width() - self.sky2_fragment.get_width()
        pos2.y = (self.position.y / 10) % self.sky2_fragment.get_height() - self.sky2_fragment.get_height()

        surf.blit(self.sky, pos1)
        surf.blit(self.sky2, pos2)
