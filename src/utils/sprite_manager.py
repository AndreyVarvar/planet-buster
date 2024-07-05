import pygame as pg


class SpriteManager:
    def __init__(self):
        self.sprites = {}  # path: image

    def add(self, name, path, animation=False, frame_dimensions=None):
        if animation:
            self.sprites.update({name: []})
            spritesheet = pg.image.load(path).convert_alpha()
            for i in range(spritesheet.width//frame_dimensions[0]):
                self.sprites[name].append(spritesheet.subsurface(pg.Rect(frame_dimensions[0]*i, 0, frame_dimensions[0], frame_dimensions[1])))
        else:
            image = pg.image.load(path).convert_alpha()
            self.sprites.update({name: image})

    def clear(self):
        self.sprites.clear()
