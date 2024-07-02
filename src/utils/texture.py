from src.utils.thingy import Thingy
import pygame as pg


class Texture(Thingy):
    def __init__(self, position, texture_path):
        super().__init__(position, pg.image.load(texture_path))


class Animation(Thingy):
    def __init__(self, position, spritesheet_path, frame_dimensions, fps=10, scale=1):
        self.generate_animation(pg.image.load(spritesheet_path), frame_dimensions, scale)

        super().__init__(position, self.animation[0])

        self.frame_idx = 0
        self.frame_count = len(self.animation)

        self.time_since_last_frame_change = 0
        self.time_between_frame_change = 1/fps

    def update(self, dt):
        self.time_since_last_frame_change += dt
        while self.time_since_last_frame_change >= self.time_between_frame_change:
            self.time_since_last_frame_change -= self.time_between_frame_change
            self.frame_idx += 1

        while self.frame_idx >= self.frame_count:
            self.frame_idx -= self.frame_count

        self.texture = self.animation[self.frame_idx]

    def generate_animation(self, spritesheet: pg.Surface, frame_dimensions, scale):
        self.animation = []

        for i in range(spritesheet.size[0]//frame_dimensions[0]):
            subsurface = spritesheet.subsurface(pg.Rect(frame_dimensions[0]*i, 0, frame_dimensions[0], frame_dimensions[1]))
            self.animation.append(pg.transform.scale_by(subsurface, scale))
