from src.utils.constants import *


def render_text_with_shadow(offset, text, colour=(255, 255, 255), drop_colour=(128, 128, 128)):
    # make the drop-shadow
    text_bitmap = default_font.render(text, True, drop_colour)

    rendered_text = pg.Surface((text_bitmap.width+offset, text_bitmap.height+offset), flags=pg.SRCALPHA)

    rendered_text.blit(text_bitmap, (offset, offset))
    # make the overlay text
    text_bitmap = default_font.render(text, True, colour)
    rendered_text.blit(text_bitmap, (0, 0))

    return rendered_text

