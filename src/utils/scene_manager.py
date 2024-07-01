class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def update(self, *args):
        self.current_scene.update(*args)

        if self.current_scene.change_scene:
            self.current_scene.change_scene = False
            new_scene = self.current_scene.change_to
            self.current_scene.change_to = None

            self.current_scene = self.scenes[new_scene]

    def draw_scene(self, *args):
        self.current_scene.draw_scene(*args)


scene_manager = SceneManager()
