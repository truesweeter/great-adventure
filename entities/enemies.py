import arcade
import math
import random
from utils import resource_path


class EnemyBeatle(arcade.Sprite):
    def __init__(self, target):
        super().__init__()
        self.target = target

        self.is_dead = False
        self.attack = True

        self.timer = 0
        self.speed = 200
        self.animation_timer = 0
        self.current_texture = 0
        self.walk_animation = [
            arcade.load_texture(resource_path("assets/enemy1/walk0.png")),
            arcade.load_texture(resource_path("assets/enemy1/walk1.png")),
            arcade.load_texture(resource_path("assets/enemy1/walk2.png")),
            arcade.load_texture(resource_path("assets/enemy1/walk3.png"))
        ]
        self.death_animation = [
            arcade.load_texture(resource_path("assets/enemy1/death0.png")),
            arcade.load_texture(resource_path("assets/enemy1/death1.png")),
            arcade.load_texture(resource_path("assets/enemy1/death2.png")),
            arcade.load_texture(resource_path("assets/enemy1/death3.png")),
            arcade.load_texture(resource_path("assets/enemy1/death4.png")),
            arcade.load_texture(resource_path("assets/enemy1/death5.png")),
            arcade.load_texture(resource_path("assets/enemy1/death6.png")),
        ]
        self.texture = self.walk_animation[0]

    def update(self, delta_time):
        if self.attack:
            dx = self.target.center_x - self.center_x
            dy = self.target.center_y - self.center_y

            distance = math.hypot(dx, dy)

            if distance > 0:
                dx /= distance
                dy /= distance

                self.center_x += dx * self.speed * delta_time
                self.center_y += dy * self.speed * delta_time

            self.animation_timer += 1

            if self.animation_timer % 8 == 0:
                self.current_texture += 1
                if self.current_texture >= len(self.walk_animation):
                    self.current_texture = 0
                self.texture = self.walk_animation[self.current_texture]

            if not self.is_dead:
                if self.target.center_x < self.center_x:
                    self.scale_x = -abs(self.scale_x)
                else:
                    self.scale_x = abs(self.scale_x)

        if self.is_dead:
            self.speed = 0
            self.animation_timer += 1

            if self.animation_timer % 8 == 0:
                self.current_texture += 1

                if self.current_texture < len(self.death_animation):
                    self.texture = self.death_animation[self.current_texture]

            self.timer += delta_time
            if self.timer >= 8:
                self.timer = 0
                self.remove_from_sprite_lists()


class EnemyZombie(arcade.Sprite):
    def __init__(self, target, collision_list):
        super().__init__()
        self.target = target
        self.collision_list = collision_list
        self.is_dead = False
        self.attack = True

        self.scale = 0.8

        self.direction = random.choice(["LEFT", "RIGHT"])

        self.timer = 0
        self.speed = 175
        self.hp = 3
        self.animation_timer = 0
        self.current_texture = 0
        self.walk_animation = [
            arcade.load_texture(resource_path("assets/enemy2/walk0.png")),
            arcade.load_texture(resource_path("assets/enemy2/walk1.png")),
            arcade.load_texture(resource_path("assets/enemy2/walk2.png")),
            arcade.load_texture(resource_path("assets/enemy2/walk3.png")),
            arcade.load_texture(resource_path("assets/enemy2/walk4.png")),
            arcade.load_texture(resource_path("assets/enemy2/walk5.png")),
            arcade.load_texture(resource_path("assets/enemy2/walk6.png")),
            arcade.load_texture(resource_path("assets/enemy2/walk7.png")),
            arcade.load_texture(resource_path("assets/enemy2/walk8.png")),
            arcade.load_texture(resource_path("assets/enemy2/walk9.png")),

        ]
        self.death_animation = [
            arcade.load_texture(resource_path("assets/enemy2/death0.png")),
            arcade.load_texture(resource_path("assets/enemy2/death1.png")),
            arcade.load_texture(resource_path("assets/enemy2/death2.png")),
            arcade.load_texture(resource_path("assets/enemy2/death3.png")),
            arcade.load_texture(resource_path("assets/enemy2/death4.png")),
            arcade.load_texture(resource_path("assets/enemy2/death5.png")),
            arcade.load_texture(resource_path("assets/enemy2/death6.png")),
        ]
        self.texture = self.walk_animation[0]

    def update(self, delta_time):
        if self.attack:
            old_x = self.center_x
            old_y = self.center_y

            dx = self.target.center_x - self.center_x
            dy = self.target.center_y - self.center_y

            distance = math.hypot(dx, dy)
            if distance == 0:
                return

            dx /= distance
            dy /= distance

            self.center_x += dx * self.speed * delta_time
            self.center_y += dy * self.speed * delta_time

            if arcade.check_for_collision_with_list(self, self.collision_list):
                self.center_x = old_x
                self.center_y = old_y

                if self.direction == "LEFT":
                    self.center_x += -dy * self.speed * 2/3 * delta_time
                    self.center_y += dx * self.speed * 2/3 * delta_time
                else:
                    self.center_x += dy * self.speed * 2/3 * delta_time
                    self.center_y += -dx * self.speed * 2/3 * delta_time



            self.physics.update()
            self.animation_timer += 1

            if self.animation_timer % 8 == 0:
                self.current_texture += 1
                if self.current_texture >= len(self.walk_animation):
                    self.current_texture = 0
                self.texture = self.walk_animation[self.current_texture]

            if not self.is_dead:
                if self.target.center_x < self.center_x:
                    self.scale_x = -abs(self.scale_x)
                else:
                    self.scale_x = abs(self.scale_x)

        if self.is_dead:
            self.speed = 0
            self.animation_timer += 1

            if self.animation_timer % 8 == 0:
                self.current_texture += 1

                if self.current_texture < len(self.death_animation):
                    self.texture = self.death_animation[self.current_texture]

            self.timer += delta_time
            if self.timer >= 8:
                self.timer = 0
                self.remove_from_sprite_lists()
