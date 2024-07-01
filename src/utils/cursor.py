import pygame as pg

class Cursor:
    def __init__(self):
        self.just_pressed = False
        self.just_released = False

        self.holding = False

        self.change_request = []

    def set_cursor(self, cursor):
        self.change_request.append(cursor)

    def update(self, mouse_pressed):
        if len(self.change_request) >= 1:
            pg.mouse.set_cursor(self.change_request[-1])
        else:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        self.change_request = []

        if mouse_pressed[0]:
            if self.just_pressed:
                self.just_pressed = False

            elif self.just_pressed is False and self.holding is False:
                self.just_pressed = True
                self.holding = True


        else:
            if self.just_released is True:
                self.just_released = False

            if self.holding:
                self.holding = False
                self.just_released = True
