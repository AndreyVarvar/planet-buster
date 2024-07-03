from src.utils.constants import *
from src.utils.thingy import Thingy

# I am afraid of this file, for I do not know the ways this files is working in to work.
# I wish luck to whoever wants to reverse engineer this pile of mess


class Slider(Thingy):
    def __init__(self,
                 position,
                 rail_size: tuple,
                 knob_size: tuple,
                 min_value: float,
                 max_value: float,
                 initial_value: float,
                 step: float):
        super().__init__(position)

        self.rail_size = rail_size
        self.knob_size = knob_size

        self.min_value = min_value
        self.max_value = max_value
        self.range = max_value - min_value

        self.initial_value = initial_value
        self.step = step

        self.slider_texture_parts = load_slider_spritesheet()


class IDK:
    def __init__(self,
                 rect: pg.Rect,
                 min_value: float,
                 max_value: float,
                 initial_value: float,
                 step: float,
                 value_rounding_accuracy=5
                 ):
        self.min_value = min_value
        self.max_value = max_value
        self.range = self.max_value - self.min_value
        self.rect = rect
        self.step = step
        self.rail = rect.inflate(0, -0.8 * rect.height)
        self.x, self.y = rect.x + rect.width*(initial_value/self.range), rect.centery
        self.clicked = False
        self.positional_step = self.rail.width / (self.range / self.step)

        self.slider_images = [pg.transform.scale_by(surf, self.rail.height/4) for surf in load_slider_spritesheet()]
        self.height = self.slider_images[6].get_height()

        self.value = initial_value
        self.value_rounding_accuracy = value_rounding_accuracy

    def calculate_slider_value(self):
        self.value = self.min_value + round((self.x - self.rail.x)*(self.range / self.rect.width), self.value_rounding_accuracy)
        self.value = max(self.min_value, min(self.max_value, self.value))

    def calculate_slider_pos(self):
        self.x = round(self.x/self.positional_step)*self.positional_step

    def update(self, mouse_pos, cursor):
        if not cursor.holding:
            self.clicked = False
        else:
            if self.clicked:
                self.clamp_rail(mouse_pos)
                self.calculate_slider_pos()
                self.calculate_slider_value()

                self.x = max(self.rail.x, min(self.x, self.rail.x + self.rail.width))  # if the position eve gets out of bounds, it will get corrected here
            else:
                if self.rect.collidepoint(mouse_pos) and cursor.just_pressed:
                    self.clicked = True

    def clamp_rail(self, mouse_pos):
        self.x = max(self.rail.left, min(mouse_pos[0], self.rail.right))

    def draw(self, surf):
        bright_part_of_slider = pg.transform.scale(self.slider_images[1], (self.x-self.rail.x, self.slider_images[1].get_height()))
        dark_side_of_slider = pg.transform.scale(self.slider_images[4], (self.rail.width - (self.x-self.rail.x), self.slider_images[4].get_height()))

        surf.blit(bright_part_of_slider, (self.rail.x, self.rail.y))
        surf.blit(self.slider_images[0], (self.rail.x, self.rail.y))

        surf.blit(dark_side_of_slider, (self.x, self.rail.y))
        surf.blit(self.slider_images[5], (self.rail.right, self.rail.y))

        surf.blit(self.slider_images[6], (self.x - self.height//2, self.y - self.height//2))



def load_slider_spritesheet():
    spritesheet = pg.image.load('assets/textures/UI/slider_spritesheet.png')

    bright_part_start = spritesheet.subsurface(pg.Rect(0, 0, 3, 8)).copy()
    bright_part_continuing = spritesheet.subsurface(pg.Rect(4, 0, 1, 8)).copy()
    bright_part_end = spritesheet.subsurface(pg.Rect(6, 0, 1, 8)).copy()

    dark_part_start = spritesheet.subsurface(pg.Rect(4, 8, 1, 8)).copy()
    dark_part_continuing = spritesheet.subsurface(pg.Rect(4, 8, 1, 8)).copy()
    dark_part_end = spritesheet.subsurface(pg.Rect(4, 8, 1, 8)).copy()

    knob = spritesheet.subsurface(pg.Rect(9, 0, 7, 16)).copy()

    slider = {
        'br_start': bright_part_start,
        'br_mid': bright_part_continuing,
        'br_end': bright_part_end,
        'dr_start': dark_part_start,
        'dr_mid': dark_part_continuing,
        'dr_end': dark_part_end,
        'knob': knob
    }

    return slider
