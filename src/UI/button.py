from src.utils.thingy import Thingy
import pygame as pg
from src.utils.constants import BLANK


class Button(Thingy):
    def __init__(self, position, size, text='', texture=BLANK, font=pg.font.SysFont('the default one', 50), text_color=(255, 255, 255)):
        super().__init__(position)

        self.pressed = False
        self.hovered = False

        self.rect = pg.Rect(position[0]-size[0]/2, position[1]-size[1]/2, size[0], size[1])

        self.text = text
        self.texture = texture

        if self.text != '':
            self.text_texture = font.render(text, True, text_color)

            self.text_pos = self.text_texture.get_rect(center=self.rect.center)

    def update(self, *args):
        mouse_pos = args[0]
        cursor = args[1]


        if self.rect.collidepoint(mouse_pos):  # update the button obviously
            self.hovered = True
            cursor.set_cursor(pg.SYSTEM_CURSOR_HAND)

            if cursor.just_released:
                self.pressed = True
            else:
                self.pressed = False
        else:
            self.hovered = False
            self.pressed = False


    def draw(self, *args):
        surf = args[0]

        if self.texture != BLANK:
            surf.blit(self.texture, self.position)
        else:
            pg.draw.rect(surf, (128, 128, 128), self.rect)

        if self.text != '':
            surf.blit(self.text_texture, self.text_pos)
