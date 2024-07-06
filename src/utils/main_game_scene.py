from src.utils.scene import Scene
from src.utils.constants import *
from math import atan2, degrees, dist
from src.utils.player import Player
from src.utils.laser import Projectile
from src.utils.enemy import Enemy
from src.utils.planet import CelestialBody
from src.utils.utilities import *
from src.utils.crosshair import CrossHair
import random
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

        # draw planets
        for planet in self.planets:
            planet.draw(surf, scroll, self.time)

        # draw projectiles
        for projectile in self.projectiles:
            projectile.draw(surf, scroll)

        # draw enemies
        for enemy in self.enemies:
            enemy.draw(surf, scroll, self.time)

        # draw the player
        self.player.draw(surf, scroll, self.time)

        # draw the crosshair
        if self.player.target_locked:
            self.crosshair.draw(surf, scroll)

        # draw other stuff
        surf.blit(render_text_with_shadow(2, f'POSITION: [{round(self.player.position.x/10)}, {round(self.player.position.y/10)}]'), (10, 10))
        # update fps
        if self.last_fps_update > self.fps_update_rate:
            self.last_fps_value = round(1/dt)
        surf.blit(render_text_with_shadow(2, f'FPS: [{self.last_fps_value}]'), (10, 50))

    def update(self, *args):
        cursor = args[1]
        dt = args[2]
        scroll = args[3]
        background = args[6]

        cursor.set_cursor(pg.SYSTEM_CURSOR_CROSSHAIR)

        # update the FPS meter
        while self.last_fps_update > self.fps_update_rate:
            self.last_fps_update -= self.fps_update_rate
        self.last_fps_update += dt

        # update the time, which is used to make some object move by using sin and cos
        self.time += dt

        # obvious updates
        self.update_planets(*args)
        self.update_crosshair(*args)
        self.update_player(*args)
        self.update_enemies(*args)
        self.update_projectiles(*args)

        # update the background according to the scroll
        background.position = -pg.Vector2(scroll)


    def update_crosshair(self, *args):
        mouse_pos = args[0]
        dt = args[2]
        scroll = args[3]
        sprite_manager = args[7]
        # update the crosshair
        self.crosshair.update(dt, sprite_manager)

        if len(self.enemies) > 0:
            closest_enemy = self.enemies[0]
            mouse_pos_in_world = pg.Vector2(mouse_pos) + pg.Vector2(scroll) - pg.Vector2(WIDTH//2, HEIGHT//2)
            for enemy in self.enemies:
                if dist(mouse_pos_in_world, enemy.position) < dist(mouse_pos_in_world, closest_enemy.position) and enemy.dead is False:
                    closest_enemy = enemy

            if dist(mouse_pos_in_world, closest_enemy.position) < 100:
                self.player.target_locked = True
                self.player.target = closest_enemy
                self.crosshair.position = closest_enemy.position
            else:
                self.player.target_locked = False
                self.player.target = None
                self.crosshair.position = (-100, -100)

    def update_enemies(self, *args):
        dt = args[2]
        scroll = args[3]
        sound_manager = args[5]
        sprite_manager = args[7]

        # update enemies
        for enemy in self.enemies.copy():
            enemy.update(dt, self.player.position, self.map_boundaries, scroll, sound_manager, sprite_manager)

            if enemy.spawn_laser and enemy.dead is False:  # spawn lasers
                self.projectiles.append(Projectile(enemy.position, 2, 1000, 180 + degrees(atan2(-enemy.position.y + self.player.position.y, enemy.position.x - self.player.position.x)), sound_manager, sprite_manager))

            if enemy.really_dead_and_should_be_destroyed:
                self.enemies.remove(enemy)

    def update_player(self, *args):
        mouse_pos = args[0]
        cursor = args[1]
        dt = args[2]
        scroll = args[3]
        keys_pressed = args[4]
        sound_manager = args[5]
        sprite_manager = args[7]

        # update the player
        self.player.update(dt, mouse_pos, scroll, keys_pressed, cursor, self.map_boundaries, sound_manager, sprite_manager)
        # spawn lasers
        if self.player.spawn_laser and self.player.dead is False:
            if self.player.target_locked:
                projectile_rotation = calculate_shoot_angle(self.player, 1000, self.player.target)
            else:
                projectile_rotation = degrees(atan2(self.player.position.y - mouse_pos[1] - scroll[1] + HEIGHT // 2, -self.player.position.x + mouse_pos[0] + scroll[0] - WIDTH // 2))

            self.projectiles.append(Projectile(self.player.position, 0, 1000, projectile_rotation, sound_manager, sprite_manager))

        # end game when player dies
        if self.player.really_dead:
            self.change_scene = True
            self.change_to = MAIN_MENU

    def update_planets(self, *args):
        dt = args[2]

        # update every planet
        for planet in self.planets:
            planet.update(dt)

            # as well as apply gravity to the player
            planet.apply_gravity(self.player, dt)
            # and the enemies
            for enemy in self.enemies:
                planet.apply_gravity(enemy, dt)

    def update_projectiles(self, *args):
        dt = args[2]
        scroll = args[3]
        sound_manager = args[5]

        # update projectiles
        for projectile in self.projectiles:
            projectile_dead = False

            projectile.update(dt)
            # make sure they are deleted in case of expired life-time
            if projectile.self_destruct:
                self.projectiles.remove(projectile)
                continue  # projectile technically does not exist anymore, so we don't need to check it against everything else

            # also make sure lasers are deleted in case of collision with a celestial body
            for planet in self.planets:
                if (planet.radius + 5) >= dist(planet.position, projectile.position):
                    self.projectiles.remove(projectile)
                    projectile_dead = True
                    break

            if projectile_dead:
                continue

            # as well as if the laser hit any other ship
            for ship in self.enemies:
                projectile_dead = False
                if (dist(projectile.position, ship.position) + 5) <= ship.hitbox_radius and projectile.type != 2 and ship.dead is False:
                    ship.health_bar.decrease()
                    self.projectiles.remove(projectile)
                    projectile_dead = True
                    # if projectile hit the enemy ship, shake the camera a little bit
                    scroll[0] += random.randint(-10, 10)
                    scroll[1] += random.randint(-10, 10)
                    sound_manager.play('hurt')
                    ship.in_pursuit = True
                    break

            if projectile_dead:
                continue

            # player ship
            if (dist(projectile.position, self.player.position) + 5) <= self.player.hitbox_radius and projectile.type != 0:
                self.player.health_bar.decrease()
                self.projectiles.remove(projectile)
                # if projectile hit the player shake the screen a lot
                scroll[0] += random.randint(-50, 50)
                scroll[1] += random.randint(-50, 50)
                sound_manager.play('hurt')
                continue

    def scene_thingies_init(self, *args):
        sprite_manager = args[0]

        sprite_manager.add('player', 'assets/textures/spritesheets/spaceship.png', True, (32, 32))
        sprite_manager.add('enemy', 'assets/textures/spritesheets/enemy-spaceship.png', True, (32, 32))
        sprite_manager.add('explosion', 'assets/textures/spritesheets/explosion.png', True, (96, 96))
        sprite_manager.add('laser', 'assets/textures/spritesheets/laser.png', True,  (32, 32))
        sprite_manager.add('crosshair', 'assets/textures/sprites/crosshair.png')

        self.crosshair = CrossHair((0, 0), sprite_manager)

        self.planets = []
        self.planets.append(CelestialBody((0, 0), 'sun', -1, sprite_manager))
        self.planets.append(CelestialBody((1000, 1000), 'gas giant', -1, sprite_manager))
        self.planets.append(CelestialBody((0, 1000), 'planet', -1, sprite_manager))
        self.planets.append(CelestialBody((-1000, 1000), 'planet', -1, sprite_manager))
        self.planets.append(CelestialBody((1000, 0), 'planet', -1, sprite_manager))


        self.player = Player((0, -1500), sprite_manager)

        self.enemies = [Enemy((-100, -1000), sprite_manager),
                        Enemy((0, -1000), sprite_manager),
                        Enemy((100, -1000), sprite_manager),
                        Enemy((-100, -1100), sprite_manager),
                        Enemy((0, -1100), sprite_manager),
                        Enemy((100, -1100), sprite_manager)]

