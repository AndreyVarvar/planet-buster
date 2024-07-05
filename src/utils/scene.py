class Scene:
    def __init__(self, name, *args):
        self.name = name
        self.change_scene = False
        self.change_to = None  # what scene to change to

        self.scene_thingies_init(*args)  # init all object in the scene

    def scene_thingies_init(self, *args):
        pass

    def draw_scene(self, *args):
        pass

    def update(self, *args):
        pass  # in here we need logic for switching scenes
