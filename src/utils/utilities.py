from src.utils.constants import *
from math import *


def render_text_with_shadow(offset, text, colour=(255, 255, 255), drop_colour=(128, 128, 128)):
    # make the drop-shadow
    text_bitmap = default_font.render(text, True, drop_colour)

    rendered_text = pg.Surface((text_bitmap.width+offset, text_bitmap.height+offset), flags=pg.SRCALPHA)

    rendered_text.blit(text_bitmap, (offset, offset))
    # make the overlay text
    text_bitmap = default_font.render(text, True, colour)
    rendered_text.blit(text_bitmap, (0, 0))

    return rendered_text


def calculate_shoot_angle(shooter, projectile_speed, target):
    v1 = projectile_speed

    try:
        v2: pg.Vector2 = target.velocity
    except AttributeError:
        v2 = pg.Vector2(0, 0)

    x1, y1 = shooter.position
    x2, y2 = target.position

    # distance between the shooter and the target
    d = sqrt((x1-x2)**2+(y1-y2)**2)

    # beta is the angle between the vector of velocity of the target and the X axis
    beta = atan2(v2.y, v2.x)
    # alpha is the angle between the vector of velocity of target and the vector from target to shooter
    alpha = atan2(y1-y2, x1-x2) - beta

    # angle between the expected trajectory of the projectile and the vector from shooter to target
    x = asin(min(1, v2.length()/v1 * sin(alpha)))

    projectile_angle = x + atan2(y2-y1, x2-x1)

    return -degrees(projectile_angle)

