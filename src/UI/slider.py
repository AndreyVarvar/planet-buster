from src.utils.constants import *
from src.utils.thingy import Thingy
from src.utils.utilities import *

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
                 step: float,
                 description='',
                 desc_with_shadow=False,
                 desc_color=ORANGE,
                 shadow_color=RED):
        super().__init__(position)

        self.rail = pg.Rect(self.position.x-rail_size[0]//2, self.position.y-rail_size[1]//2, rail_size[0], rail_size[1])  # rail rect
        self.knob = pg.Rect(self.position.x-knob_size[0]//2, self.position.y-knob_size[1]//2, knob_size[0], knob_size[1])  # knob rect

        self.min_value = min_value
        self.max_value = max_value
        self.range = max_value - min_value

        self.prev_value = initial_value

        self.initial_value = initial_value
        self.step = step

        self.slider_texture_parts = load_slider_spritesheet()
        # scale each part appropriately
        scale_factor = rail_size[1]/self.slider_texture_parts['br'].get_size()[1]

        for part in ['br', 'dr', 'br_start', 'dr_end']:
            img = self.slider_texture_parts[part]
            self.slider_texture_parts[part] = pg.transform.scale_by(img, scale_factor)

        knob = self.slider_texture_parts['knob']
        self.slider_texture_parts['knob'] = pg.transform.scale_by(knob, knob_size[1] / knob.get_size()[1])


        self.positional_step = self.rail.width / (self.range / self.step)

        self.knob_pos = pg.Vector2(self.rail.x + self.rail.width*(initial_value/self.range), self.rail.centery)

        self.knob_size = self.slider_texture_parts['knob'].get_size()

        self.value = initial_value

        self.clicked = False

        if desc_with_shadow:
            self.description = render_text_with_shadow(2, description, desc_color, shadow_color)
        else:
            self.description = default_font.render(description, True, desc_color)

    def update(self, mouse_pos, cursor, sound_manager):
        if not cursor.holding:
            self.clicked = False
        else:
            if self.clicked:
                self.clamp_rail(mouse_pos)
                self.calculate_knob_pos()
                self.calculate_slider_value()

                self.knob_pos.x = max(self.rail.x, min(self.knob_pos.x, self.rail.x + self.rail.width))  # if the position eve gets out of bounds, it will get corrected here
            else:
                if self.rail.collidepoint(mouse_pos) and cursor.just_pressed:
                    self.clicked = True

        if self.value != self.prev_value:
            self.prev_value = self.value
            sound_manager.play('ui-slider-slide')

    def draw(self, *args):
        surf = args[0]

        # step 1: draw the bright side (the left one)
        bright = self.slider_texture_parts['br']
        bright_start = self.slider_texture_parts['br_start']

        duration = round(self.knob_pos.x - self.rail.x)

        for i in range(bright_start.get_size()[0], duration):
            surf.blit(bright, (self.rail.x+i, self.position.y-self.rail.height//2))

        surf.blit(bright_start, (self.rail.x, bright_start.get_size()[0]+self.position.y - self.rail.height // 2))

        # step 2: draw the dark side
        dark = self.slider_texture_parts['dr']
        dark_end = self.slider_texture_parts['dr_end']

        duration = round(self.rail.x + self.rail.width - self.knob_pos.x)

        for i in range(duration):
            surf.blit(dark, (self.rail.x+self.rail.width-i, self.position.y-self.rail.height//2))

        surf.blit(dark_end, (self.rail.x+self.rail.width+dark_end.get_size()[0], dark_end.get_size()[0] + self.position.y - self.rail.height // 2))

        # step 3: draw the knob
        knob = self.slider_texture_parts['knob']

        pos = knob.get_rect(center=self.knob_pos)

        surf.blit(knob, pos)

        # draw description
        pos = self.description.get_rect(center=(self.position.x, self.position.y-self.knob_size[1]-20))
        surf.blit(self.description, pos)

    def clamp_rail(self, mouse_pos):
        # adjust the knob position to the mouse position, but also makes sure we don't bring it outside the min and max values
        self.knob_pos.x = max(self.rail.left, min(mouse_pos[0], self.rail.right))

    def calculate_slider_value(self):
        # based on position, calculates what value it has
        self.value = self.min_value + round((self.knob_pos.x - self.rail.x - 1)*(self.range / self.rail.width), 1)
        self.value = max(self.min_value, min(self.max_value, self.value))

    def calculate_knob_pos(self):
        self.knob_pos.x = self.rail.x + round((self.knob_pos.x-self.rail.x)/self.positional_step)*self.positional_step  # round to the nearest 'step' value


def load_slider_spritesheet():
    spritesheet = pg.image.load('assets/textures/UI/slider_spritesheet.png')

    bright_side = spritesheet.subsurface(pg.Rect(14, 0, 1, 10)).copy()
    bright_side_start = spritesheet.subsurface(pg.Rect(15, 1, 1, 8)).copy()

    dark_side = spritesheet.subsurface(pg.Rect(12, 0, 1, 10)).copy()
    dark_side_start = spritesheet.subsurface(pg.Rect(11, 1, 1, 8)).copy()

    knob = spritesheet.subsurface(pg.Rect(0, 0, 10, 10)).copy()

    slider = {
        'br': bright_side,
        'dr': dark_side,
        'br_start': bright_side_start,
        'dr_end': dark_side_start,
        'knob': knob
    }

    return slider
