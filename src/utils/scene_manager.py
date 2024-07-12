from src.utils.constants import *


class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

        self.leaving = False

        self.font = None

    def update(self, *args):
        sound_manager = args[5]
        sprite_manager = args[7]
        music_manager = args[8]
        difficulty = args[9]

        self.current_scene.update(*args)

        if self.current_scene.change_scene:
            self.current_scene.change_scene = False

            if self.current_scene.change_to != 'quit':
                new_scene = self.current_scene.change_to
                self.current_scene.change_to = None

                sprite_manager.clear()  # we have some sprites we won't use anymore, so it is best to get rid of them, especially if these sprites are a collection of planet animations ranging in the hundreds of individual frames
                self.current_scene = self.scenes[new_scene](sprite_manager, sound_manager, music_manager, difficulty)
            else:
                self.leaving = True

    def draw_scene(self, *args):
        self.current_scene.draw_scene(*args)

    def add_scene(self, name, scene):
        self.scenes.update({name: scene})
