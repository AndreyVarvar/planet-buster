from src.utils.scene import Scene
from math import atan2, degrees, dist
from src.utils.game_files.player import Player
from src.utils.game_files.laser import Projectile
from src.utils.game_files.enemy import Enemy
from src.utils.utilities import *
from src.utils.game_files.crosshair import CrossHair
from src.utils.game_files.radar import Radar
from src.utils.game_files.map_generator import generate_map
from src.utils.game_files.planet_buster import PlanetBuster
import random
# here lies the massive scene that is out game


class MainGame(Scene):
    def __init__(self, *args):
        sprite_manager = args[0]
        super().__init__(MAIN_GAME, *args)

        self.map_boundaries = pg.Rect(-10_000, -10_000, 20_000, 20_000)

        self.planet_buster = None

        self.time = 0

        self.projectiles = []

        self.mission_failed = False
        self.end_of_mission = False

        self.fps_update_rate = 1  # every second
        self.last_fps_update = 0
        self.last_fps_value = 100
        self.radar = Radar(self.player.position, sprite_manager)

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

        # draw planet buster
        if self.planet_buster is not None:
            self.planet_buster.draw(surf, scroll)

        # draw the player
        self.player.draw(surf, scroll, self.time)

        # draw the crosshair
        if self.player.target_locked:
            self.crosshair.draw(surf, scroll)

        # draw the radar
        self.radar.draw(surf, scroll, offset=pg.Vector2(WIDTH//2 - 140, -HEIGHT//2 + 140))

        self.draw_special_text(surf, dt, self.player)

    def update(self, *args):
        cursor = args[1]
        dt = args[2]
        scroll = args[3]
        background = args[6]
        sprite_manager = args[7]

        cursor.set_cursor(pg.SYSTEM_CURSOR_CROSSHAIR)

        # update the FPS meter
        while self.last_fps_update > self.fps_update_rate:
            self.last_fps_update -= self.fps_update_rate
        self.last_fps_update += dt

        # update the time, which is used to make some object move by using sin and cos
        self.time += dt

        # obvious updates
        self.update_radar(*args)
        self.update_planets(*args)
        self.update_crosshair(*args)
        self.update_player(*args)
        self.update_enemies(*args)
        self.update_projectiles(*args)

        # check if planet buster is called on
        self.deploy_planet_buster(sprite_manager, dt)

        # update the background according to the scroll
        background.position = -pg.Vector2(scroll)

    def deploy_planet_buster(self, *args):
        sprite_manager = args[0]
        dt = args[1]

        # make planet buster if called, otherwise just update
        if self.planet_buster is not None:
            self.planet_buster.update(dt)
        elif self.player.fire_planet_buster and self.player.used_the_only_attempt is False:
            self.player.used_the_only_attempt = True
            self.planet_buster = PlanetBuster(self.player.position, sprite_manager)

            # get the target
            closest_planet = self.planets[1]
            for planet in self.planets[1:]:
                if dist(self.planet_buster.position, planet.position) < dist(self.planet_buster.position, closest_planet.position):
                    closest_planet = planet

            self.planet_buster.target = closest_planet

        # check any collisions
        if self.planet_buster is not None:
            for planet in self.planets:
                if dist(self.planet_buster.position, planet.position) <= (planet.radius+10):
                    self.planet_buster = None
                    planet.destroyed = True
                    self.end_of_mission = True
                    if not planet.target:
                        self.mission_failed = True
                    break

    def update_radar(self, *args):
        scroll = args[3]
        sprite_manager = args[7]
        self.radar.position = pg.Vector2(scroll)
        self.radar.update(self.player, self.planets, self.enemies, sprite_manager, pg.Vector2(WIDTH//2 - 140, -HEIGHT//2 + 140))

    def update_crosshair(self, *args):
        mouse_pos = args[0]
        dt = args[2]
        scroll = args[3]
        sprite_manager = args[7]

        # update the crosshair
        self.crosshair.update(dt, self.player, self.enemies, self.planets, mouse_pos, scroll, sprite_manager)

    def update_enemies(self, *args):
        dt = args[2]
        scroll = args[3]
        sound_manager = args[5]
        sprite_manager = args[7]

        # update enemies
        for enemy in self.enemies.copy():
            enemy.update(dt, self.player.position, self.map_boundaries, scroll, sound_manager, sprite_manager)

            if enemy.spawn_laser and enemy.dead is False:  # spawn lasers
                projectile_angle = calculate_shoot_angle(enemy, 1000, self.player) + random.randint(-10, 10)
                self.projectiles.append(Projectile(enemy.position, 2, 1000, projectile_angle, sound_manager, sprite_manager))

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
        self.player.update(dt, mouse_pos, scroll, keys_pressed, cursor, self.map_boundaries, sound_manager, sprite_manager, self.crosshair)
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
        sprite_manager.add('planet buster', 'assets/textures/sprites/planet_buster.png')
        sprite_manager.add('exploding planet', 'assets/textures/spritesheets/exploding_planet.png', True, (96, 96))

        self.crosshair = CrossHair((0, 0), sprite_manager)

        self.planets = generate_map(sprite_manager, 1)


        self.player = Player((0, -1500), sprite_manager)

        self.enemies = [Enemy((0, -1100), sprite_manager),
                        Enemy((50, -1100), sprite_manager),
                        Enemy((100, -1100), sprite_manager),
                        Enemy((150, -1100), sprite_manager),
                        Enemy((200, -1100), sprite_manager),
                        Enemy((250, -1100), sprite_manager),
                        Enemy((300, -1100), sprite_manager),
                        Enemy((350, -1100), sprite_manager),
                        Enemy((400, -1100), sprite_manager),
                        Enemy((450, -1100), sprite_manager),]

    def draw_special_text(self, *args):
        surf = args[0]
        dt = args[1]
        player = args[2]

        # display position
        surf.blit(render_text_with_shadow(2, f'POSITION: [{round(self.player.position.x / 10)}, {round(self.player.position.y / 10)}]'), (10, 10))
        # display fps
        if self.last_fps_update > self.fps_update_rate:
            self.last_fps_value = round(1 / dt)
        surf.blit(render_text_with_shadow(2, f'FPS: [{self.last_fps_value}]'), (10, 50))

        # display planet buster status
        if player.used_the_only_attempt:
            surf.blit(render_text_with_shadow(2, '[PLANET BUSTER DEPLOYED]', colour=ORANGE, drop_colour=RED), (10, 90))
        elif player.planet_buster_activated:
            surf.blit(render_text_with_shadow(2, f'[PLANET BUSTER ACTIVATION IN:]', colour=YELLOW, drop_colour=ORANGE), (10, 90))
            surf.blit(render_text_with_shadow(2, f'[{ceil(player.planet_buster_activation_time)} SECONDS]', colour=YELLOW, drop_colour=ORANGE), (10, 130))
        else:
            surf.blit(render_text_with_shadow(2, f'[PLANET BUSTER ONLINE]', colour=GREEN, drop_colour=DARK_GREEN), (10, 90))

        # draw mission details
        if self.end_of_mission:
            if self.mission_failed:
                surf.blit(render_text_with_shadow(2, f'[MISSION FAILED]', colour=RED, drop_colour=DARK_RED), (10, 130))
            else:
                surf.blit(render_text_with_shadow(2, f'[MISSION SUCCESSFUL]', colour=GREEN, drop_colour=DARK_GREEN), (10, 130))
