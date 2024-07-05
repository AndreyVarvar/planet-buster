from src.utils.thingy import Thingy


class Animation(Thingy):
    def __init__(self, position, animation_name, sprite_manager, fps=10, scale=1, drawing_rotation=0):
        self.animation = sprite_manager.sprites[animation_name]
        super().__init__(position, self.animation[0], scale=scale, drawing_angle_offset=drawing_rotation)

        self.frame_idx = 0
        self.frame_count = len(self.animation)

        self.time_since_last_frame_change = 0
        self.time_between_frame_change = 1/fps

        self.animation_end = False

    def update(self, dt):
        self.time_since_last_frame_change += dt
        while self.time_since_last_frame_change >= self.time_between_frame_change:
            self.time_since_last_frame_change -= self.time_between_frame_change
            self.frame_idx += 1

        self.animation_end = False
        while self.frame_idx >= self.frame_count:  # I know I could have used '%', but forgot
            self.frame_idx -= self.frame_count
            self.animation_end = True

        self.texture = self.animation[self.frame_idx]
