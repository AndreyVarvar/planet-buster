from src.utils.scene import Scene
from src.utils.constants import *
from math import atan2, degrees, dist
from src.utils.player import Player
from src.utils.laser import Projectile
from src.utils.enemy import Enemy
from src.utils.planet import CelestialBody
from src.utils.utilities import render_text_with_shadow
# here lies the massive scene that is out game


class MainGame(Scene):
    def __init__(self, *args):
        super().__init__(MAIN_GAME, *args)

        self.map_boundaries = pg.Rect(-10_000, -10_000, 20_000, 20_000)

        self.time = 0

        self.projectiles = []

        self.fps_update_rate = 1  # every second
        self.last_fps_update = 0
        self.last_fps_value = 100

        self.game_end = False

    def draw_scene(self, *args):
        surf = args[0]
        dt = args[1]
        scroll = args[2]

        for planet in self.planets:
            planet.draw(surf, scroll, self.time)

        for projectile in self.projectiles:
            projectile.draw(surf, scroll)

        for enemy in self.enemies:
            enemy.draw(surf, scroll, self.time)

        self.player.draw(surf, scroll, self.time)

        surf.blit(render_text_with_shadow(2, f'POSITION: [{round(self.player.position.x/10)}, {round(self.player.position.y/10)}]'), (10, 10))

        # update fps
        if self.last_fps_update > self.fps_update_rate:
            self.last_fps_value = round(1/dt)
        surf.blit(render_text_with_shadow(2, f'FPS: [{self.last_fps_value}]'), (10, 50))

    def update(self, *args):
        mouse_pos = args[0]
        cursor = args[1]
        dt = args[2]
        scroll = args[3]
        keys_pressed = args[4]
        sound_manager = args[5]
        background = args[6]
        sprite_manager = args[7]

        # update the FPS meter
        while self.last_fps_update > self.fps_update_rate:
            self.last_fps_update -= self.fps_update_rate
        self.last_fps_update += dt

        # update the time, which is used to make some object move by using sin and cos
        self.time += dt

        self.update_objects_that_affect_surroundings(*args)

        # update the background according to the scroll
        background.position = -pg.Vector2(scroll)

        # update the player
        self.player.update(dt, mouse_pos, scroll, keys_pressed, cursor, self.map_boundaries, sound_manager, sprite_manager)

        # update enemies
        for enemy in self.enemies.copy():
            enemy.update(dt, self.player.position, self.map_boundaries, scroll, sound_manager, sprite_manager)

            if enemy.spawn_laser:  # spawn lasers
                self.projectiles.append(Projectile(enemy.position, 2, 1000, 20, 180+degrees(atan2(-enemy.position.y+self.player.position.y, enemy.position.x-self.player.position.x)), sound_manager, sprite_manager))

            if enemy.really_dead_and_should_be_destroyed:
                self.enemies.remove(enemy)
        # spawn lasers
        if self.player.spawn_laser:
            self.projectiles.append(Projectile(self.player.position, 0, 1000, 100, degrees(atan2(self.player.position.y-mouse_pos[1]-scroll[1]+HEIGHT//2, -self.player.position.x+mouse_pos[0]+scroll[0]-WIDTH//2)), sound_manager, sprite_manager))

        # end game when player dies
        if self.player.really_dead:
            self.change_scene = True
            self.change_to = MAIN_MENU

    def update_objects_that_affect_surroundings(self, *args):
        mouse_pos = args[0]
        cursor = args[1]
        dt = args[2]
        scroll = args[3]
        keys_pressed = args[4]
        sound_manager = args[5]
        background = args[6]
        sprite_manager = args[7]

        # update every planet
        for planet in self.planets:
            planet.update(dt)

            # as well as apply gravity to the player
            planet.apply_gravity(self.player, dt)
            # and the enemies
            for enemy in self.enemies:
                planet.apply_gravity(enemy, dt)

        # update projectiles
        for projectile in self.projectiles.copy():
            projectile.update(dt)
            # make sure they are deleted in case of expired life-time
            if projectile.self_destruct:
                self.projectiles.remove(projectile)
                continue

            # also make sure lasers are deleted in case of collision with a celestial body
            for planet in self.planets:
                if (planet.radius + 5) >= dist(planet.position, projectile.position):
                    self.projectiles.remove(projectile)
                    continue


    def scene_thingies_init(self, *args):
        sprite_manager = args[0]

        sprite_manager.add('player', 'assets/textures/spritesheets/spaceship.png', True, (32, 32))
        sprite_manager.add('enemy', 'assets/textures/spritesheets/enemy-spaceship.png', True, (32, 32))
        sprite_manager.add('explosion', 'assets/textures/spritesheets/explosion.png', True, (96, 96))
        sprite_manager.add('laser', 'assets/textures/spritesheets/laser.png', True,  (32, 32))

        self.planets = []
        self.planets.append(CelestialBody((0, 0), 'sun', -1, sprite_manager))
        self.planets.append(CelestialBody((1000, 1000), 'planet', 6, sprite_manager))
        self.planets.append(CelestialBody((0, 1000), 'planet', 7, sprite_manager))
        self.planets.append(CelestialBody((-1000, 1000), 'planet', 8, sprite_manager))
        self.planets.append(CelestialBody((1000, 0), 'planet', -1, sprite_manager))


        self.player = Player((500, 500), sprite_manager)

        self.enemies = [Enemy((-100, -1000), sprite_manager),
                        Enemy((0, -1000), sprite_manager),
                        Enemy((100, -1000), sprite_manager),
                        Enemy((-100, -1100), sprite_manager),
                        Enemy((0, -1100), sprite_manager),
                        Enemy((100, -1100), sprite_manager)]

