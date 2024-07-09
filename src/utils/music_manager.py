import pygame as pg


class MusicManager:
    def __init__(self):
        self.current_music = None
        self.musics = {}
        self.volume = 0

    def add(self, name, path):
        self.musics.update({name: path})

    def play(self, name):
        if self.volume != 0:
            if self.current_music != name:
                pg.mixer.music.stop()
                self.current_music = name
                pg.mixer.music.load(self.musics[name])
                pg.mixer.music.set_volume(self.volume)
                pg.mixer.music.play()
            else:
                if not pg.mixer.music.get_busy():
                    pg.mixer.music.set_volume(self.volume)
                    pg.mixer.music.play()
        else:
            pg.mixer.music.stop()

    def set_volume(self, volume):
        self.volume = volume
        pg.mixer.music.set_volume(self.volume)
