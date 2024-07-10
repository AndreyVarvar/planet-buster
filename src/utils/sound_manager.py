from random import choice
import pygame as pg


class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.volume = 1

    def add(self, name, sound, type='singular'):
        if type == 'singular':
            self.sounds.update({name: sound})
        elif type == 'multiple':
            self.sounds.update({name: []})
            for s in sound:
                self.sounds[name].append(s)


    def play(self, sound, loop=0):
        s = self.sounds[sound]

        if isinstance(s, list):
            choice(s).play(loops=loop)
        else:
            s.play(loops=loop)

    def stop(self, sound):
        s = self.sounds[sound]

        if isinstance(s, list):
            for sound in s:
                sound.stop()
        else:
            s.stop()

    def stop_all(self):
        for sound in self.sounds:
            s = self.sounds[sound]

            if isinstance(s, list):
                for sfx in s:
                    sfx.stop()
            else:
                s.stop()

    def set_volume(self, volume):
        self.volume = volume
        for name in self.sounds:
            sound = self.sounds[name]
            if isinstance(sound, list):
                for s in sound:
                    s.set_volume(volume)
            else:
                sound.set_volume(volume)

