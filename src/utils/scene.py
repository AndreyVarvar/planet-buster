class Scene:
    def __init__(self, name, scene_manager):
        self.name = name
        self.change_scene = False
        self.change_to = None  # what scene to change to

        self.scene_thingies_init()  # init all object in the scene

        scene_manager.scenes.update({name: self})

    def scene_thingies_init(self, *args):
        pass

    def draw_scene(self, *args):
        pass

    def update(self, *args):
        pass  # in here we need logic for switching scenes

    def reset(self, *args):
        pass  # what happens when we load the scene, maybe resetting a bunch of stuff, idk
