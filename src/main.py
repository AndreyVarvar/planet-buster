import pygame as pg
pg.init()

from src.utils.scene_manager import scene_manager  # crazy namings
from src.utils.constants import *

from src.utils.cursor import Cursor


class Game:
    def __init__(self, display_size):
        self.display_size = display_size
        self.display = pg.display.set_mode(display_size)
        self.running = True

        self.scene_manager = scene_manager
        self.scene_manager.current_scene = scene_manager.scenes['main menu']

        self.clock = pg.time.Clock()

        self.cursor = Cursor()

    def run(self):
        while self.running:
            events = pg.event.get()

            self.event_handling(events)  # handle events bruh
            self.update()
            self.draw()

            self.clock.tick(FPS)

    def event_handling(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False

    def draw(self):
        self.scene_manager.draw_scene(self.display)

        pg.display.update()

    def update(self):
        self.scene_manager.update(pg.mouse.get_pos(), self.cursor)

        self.cursor.update(pg.mouse.get_pressed())

