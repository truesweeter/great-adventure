import arcade
import random

from config import *
from utils import resource_path
from entities.hero import Hero
from entities.enemies import EnemyBeatle, EnemyZombie
from entities.items import *
from views.pause_view import PauseView
from views.death_view import DeathView


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.keys_pressed = []
        self.timer = 0
        self.game_time = 0
        self.kill_count = 0
        self.time_survived = 0.0
        self.player_list = arcade.SpriteList()
        self.player = Hero()
        self.player_list.append(self.player)

        self.bullets = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.items = arcade.SpriteList()

        tile_map = arcade.load_tilemap(resource_path('map.tmx'), scaling=0.6)
        self.box_list = tile_map.sprite_lists['boxes']
        self.ground_list = tile_map.sprite_lists['ground']
        self.walls_list = tile_map.sprite_lists['walls']
        self.collision_list = tile_map.sprite_lists['collision']
        self.gates = tile_map.sprite_lists['gates']
        self.hero_col = tile_map.sprite_lists['col_hero']
        self.player_physics = arcade.PhysicsEngineSimple(self.player, self.hero_col)
        self.gate_positions = [(gate.center_x, gate.center_y) for gate in self.gates]

        self.camera = arcade.camera.Camera2D()
        self.ui_camera = arcade.camera.Camera2D()
        self.pick_up_sound = arcade.load_sound(resource_path("assets/sounds/pick_up.mp3"))
        self.nuke_sound = arcade.load_sound(resource_path("assets/sounds/nuke.mp3"))

        skull = arcade.Sprite(resource_path('assets/kills.png'))
        skull.scale = 1
        skull.center_x = 20
        skull.center_y = 60
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(skull)

        watch = arcade.Sprite(resource_path('assets/watch.png'))
        watch.scale = 0.12
        watch.center_x = 20
        watch.center_y = 20
        self.all_sprites.append(watch)

        self.soundtrack = arcade.load_sound(resource_path("assets/sounds/soundtrack.mp3"))
        self.soundtrack_player = None
        self.soundtrack_started = False
        self.sound_timer = 0

    def setup(self):
        self.keys_pressed = set()
        self.timer = 0

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.ground_list.draw()
        self.walls_list.draw()
        self.box_list.draw()
        self.enemies.draw()
        self.player_list.draw()
        self.bullets.draw()
        self.items.draw()
        arcade.draw_text(
            f"Убийства: {self.kill_count}",
            self.camera.position.x - SCREEN_WIDTH // 2 + 40,
            self.camera.position.y - SCREEN_HEIGHT // 2 + 50,
            arcade.color.WHITE,
            16,
            font_name="Minecraft Rus"
        )

        arcade.draw_text(
            f"Время: {int(self.time_survived)} c",
            self.camera.position.x - SCREEN_WIDTH // 2 + 40,
            self.camera.position.y - SCREEN_HEIGHT // 2 + 10,
            arcade.color.WHITE,
            16,
            font_name="Minecraft Rus"
        )
        self.ui_camera.use()
        self.all_sprites.draw()

    def on_update(self, delta_time):
        if not self.soundtrack_started:
            self.sound_timer += delta_time
            if self.sound_timer > 1.5:
                self.soundtrack_player = self.soundtrack.play(
                    volume=0.3,
                    loop=True
                )
                self.soundtrack_started = True


        self.time_survived += delta_time

        self.player.update(self.keys_pressed, delta_time, self.bullets)
        self.player_physics.update()
        self.bullets.update(delta_time)
        self.enemies.update(delta_time)
        self.items.update(delta_time)

        # спавн врагов
        self.game_time += delta_time
        self.timer += delta_time

        wave = int(self.game_time // 65)

        if wave == 0:
            spawn_chance = 0.4
            zombie_chance = 0.30
        elif wave == 1:
            spawn_chance = 0.6
            zombie_chance = 0.35
        else:
            spawn_chance = 0.7
            zombie_chance = 0.4
        

        if self.timer >= 1:
            if random.random() < spawn_chance:
                if random.random() < zombie_chance:
                    enemy = EnemyZombie(self.player, self.collision_list)
                    enemy.physics = arcade.PhysicsEngineSimple(enemy, self.collision_list)
                else:
                    enemy = EnemyBeatle(self.player)

                self.timer = 0
                position = random.randint(0, 1)

                cam_x = self.camera.position.x
                cam_y = self.camera.position.y
                offset = 50

                if enemy.__class__ == EnemyZombie:
                    x, y = random.choice(self.gate_positions)
                    enemy.center_x = x
                    enemy.center_y = y

                else:
                    if position == 0:
                        enemy.center_y = random.randint(
                            int(cam_y - SCREEN_HEIGHT / 2),
                            int(cam_y + SCREEN_HEIGHT / 2)
                        )
                        enemy.center_x = random.choice([
                            int(cam_x - SCREEN_WIDTH / 2 - offset),
                            int(cam_x + SCREEN_WIDTH / 2 + offset)
                        ])
                    else:
                        enemy.center_x = random.randint(
                            int(cam_x - SCREEN_WIDTH / 2),
                            int(cam_x + SCREEN_WIDTH / 2)
                        )
                        enemy.center_y = random.choice([
                            int(cam_y - SCREEN_HEIGHT / 2 - offset),
                            int(cam_y + SCREEN_HEIGHT / 2 + offset)
                        ])

                self.enemies.append(enemy)

            self.timer = 0

        # попадение выстрела в жука
        for bullet in self.bullets:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies)
            for enemy in hit_list:
                if not enemy.is_dead:
                    bullet.remove_from_sprite_lists()
                if not enemy.is_dead:
                    if isinstance(enemy, EnemyBeatle):
                        enemy.is_dead = True
                        self.kill_count += 1
                        enemy.animation_timer = 0
                        enemy.current_texture = 0
                        enemy.texture = enemy.death_animation[0]
                    if isinstance(enemy, EnemyZombie):
                        if enemy.hp > 1:
                            enemy.hp -= 1
                        else:
                            enemy.is_dead = True
                            self.kill_count += 1
                            enemy.animation_timer = 0
                            enemy.current_texture = 0
                            enemy.texture = enemy.death_animation[0]

                    # выпадение предметов с врагов
                    if enemy.is_dead:
                        drop = random.choice(
                            [False, False, False, False, False, True]  # шанс появления предмета 16%
                        )
                        # шансы появления
                        # перец - 33%
                        # дробовик - 25%
                        # двойные пистолеты - 17%
                        # автоматическая стрельба - 17%
                        # ядерка - 8%
                        if drop:
                            items = (
                                Pepper, Pepper, Pepper, Pepper,
                                DoubleBarreled, DoubleBarreled, DoubleBarreled,
                                DoublePistols, DoublePistols,
                                Autogun, Autogun,
                                Nuke,
                            )
                            item_name = random.choice(items)
                            item = item_name()
                            item.center_x = enemy.center_x
                            item.center_y = enemy.center_y
                            self.items.append(item)
                            if len(self.items) > 2:  # максимум два предмета на карте
                                self.items[0].remove_from_sprite_lists()

        # подбор предмета
        picked_items = arcade.check_for_collision_with_list(self.player, self.items)
        for item in picked_items:
            item.remove_from_sprite_lists()
            self.play_pick_up_sound(item)
            self.player.get_buff(item)
            if item.buff == 'nuke':  # подбор игроком ядерки
                for enemy in self.enemies:
                    if enemy.is_dead == False:
                        enemy.is_dead = True
                        self.kill_count += 1
                        enemy.animation_timer = 0
                        enemy.current_texture = 0
                        enemy.texture = enemy.death_animation[0]

        # попадание пули в стену
        for bullet in self.bullets:
            if arcade.check_for_collision_with_list(bullet, self.collision_list):
                bullet.remove_from_sprite_lists()

        # смерть героя
        hit_list = arcade.check_for_collision_with_list(self.player, self.enemies)
        for enemy in hit_list:
            if not enemy.is_dead:
                death_view = DeathView(self.kill_count, self.time_survived)
                #стоп музыки
                if self.soundtrack_player:
                    self.soundtrack_player.pause()
                    self.soundtrack_player = None
                self.window.show_view(death_view)
        

        self.center_camera()

    def center_camera(self):
        screen_center_x = self.player.center_x
        screen_center_y = self.player.center_y
        screen_center_x = max(0, screen_center_x)
        screen_center_y = max(0, screen_center_y)
        self.camera.position = (screen_center_x, screen_center_y)

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_key_press(self, key, modifiers):
        self.keys_pressed.append(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

        #переход в паузу
        if key == arcade.key.ESCAPE:
            self.soundtrack_player.pause()
            self.window.show_view(PauseView(self))

    def on_hide_view(self):
        self.keys_pressed.clear()

    def play_pick_up_sound(self, item):
        if item.buff == "nuke":
            arcade.play_sound(self.nuke_sound)
        else:
            arcade.play_sound(self.pick_up_sound)
    
    def on_show_view(self):
        if self.soundtrack_player:
            self.soundtrack_player.play()
