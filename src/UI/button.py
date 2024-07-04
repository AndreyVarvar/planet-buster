from src.utils.thingy import Thingy
from src.utils.constants import *
from src.utils.utilities import render_text_with_shadow

class Button(Thingy):
    def __init__(self, position, size, text='', texture=BLANK, hover_texture=BLANK, font=pg.font.SysFont('the default one', 50), text_color=(255, 255, 255), text_with_shadow=False, shadow_color=(128, 128, 128)):
        super().__init__(position)

        self.pressed = False
        self.hovered = False

        self.rect = pg.Rect(position[0]-size[0]/2, position[1]-size[1]/2, size[0], size[1])

        self.text = text
        self.texture = texture
        self.hover_texture = hover_texture


        if self.text != '':
            if text_with_shadow:
                self.text_texture = render_text_with_shadow(2, text, text_color, shadow_color)
            else:
                self.text_texture = font.render(text, True, text_color)

            self.text_pos = self.text_texture.get_rect(center=self.rect.center)

    def update(self, *args):
        mouse_pos = args[0]
        cursor = args[1]
        sound_manager = args[2]


        if self.rect.collidepoint(mouse_pos) and not self.hovered:  # update the button
            self.hovered = True

            sound_manager.play('ui-button-hover')

        elif not self.rect.collidepoint(mouse_pos):
            self.hovered = False
            self.pressed = False

        if self.hovered:
            cursor.set_cursor(pg.SYSTEM_CURSOR_HAND)

        if cursor.just_released and self.hovered:
            self.pressed = True
            sound_manager.play('ui-button-click')
        else:
            self.pressed = False


    def draw(self, *args):
        surf = args[0]

        pos = self.texture.get_rect(center=self.position)

        if self.texture != BLANK:
            surf.blit(self.texture, pos)
        else:
            pg.draw.rect(surf, (128, 128, 128), self.rect)

        if self.hovered and self.hover_texture != BLANK:
            surf.blit(self.hover_texture, pos)

        if self.text != '':
            surf.blit(self.text_texture, self.text_pos)
