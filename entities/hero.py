import arcade
from config import *
from utils import resource_path
from entities.bullet import Bullet


class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2

        self.speed = 200
        self.scale = 1

        self.double_barreled = False
        self.auto = False
        self.auto_timer = 0
        self.auto_cooldown = 2.5

        self.speed_buff_timer = 0
        self.double_buff_timer = 0
        self.shoot_speed_buff_timer = 0
        self.auto_buff_timer = 0

        self.walk_down = [
            arcade.load_texture(resource_path("assets/hero/down0.png")),
            arcade.load_texture(resource_path("assets/hero/down1.png")),
            arcade.load_texture(resource_path("assets/hero/down2.png")),
            arcade.load_texture(resource_path("assets/hero/down3.png"))
        ]

        self.walk_up = [
            arcade.load_texture(resource_path("assets/hero/up0.png")),
            arcade.load_texture(resource_path("assets/hero/up1.png")),
            arcade.load_texture(resource_path("assets/hero/up2.png")),
            arcade.load_texture(resource_path("assets/hero/up3.png"))
        ]

        self.walk_right = [
            arcade.load_texture(resource_path("assets/hero/right0.png")),
            arcade.load_texture(resource_path("assets/hero/right1.png")),
            arcade.load_texture(resource_path("assets/hero/right2.png")),
            arcade.load_texture(resource_path("assets/hero/right3.png"))
        ]

        self.walk_left = [
            arcade.load_texture(resource_path("assets/hero/left0.png")),
            arcade.load_texture(resource_path("assets/hero/left1.png")),
            arcade.load_texture(resource_path("assets/hero/left2.png")),
            arcade.load_texture(resource_path("assets/hero/left3.png"))
        ]

        self.current_texture = 0
        self.animation_timer = 0
        self.texture = self.walk_down[0]
        self.direction = "down"

        self.shoot_timer = 0
        self.shoot_cooldown = 0.5

        self.shot_sound = arcade.load_sound(
            resource_path("assets/sounds/shot.wav")
        )
        self.shot2_sound = arcade.load_sound(
            resource_path("assets/sounds/shot2.wav")
        )

    def get_buff(self, item):
        if item.buff == 'speed':
            self.speed = 275
            self.speed_buff_timer = 8
        if item.buff == 'double':
            self.double_barreled = True
            self.double_buff_timer = 5
        if item.buff == 'shoot_speed':
            self.shoot_cooldown = 0.25
            self.shoot_speed_buff_timer = 5
        if item.buff == 'auto':
            self.auto = True
            self.auto_buff_timer = 11

    def update(self, keys_pressed, delta_time, bullets):
        self.keys_pressed = keys_pressed
        moving = False

        if self.shoot_timer > 0:
            self.shoot_timer -= delta_time

        if arcade.key.W in self.keys_pressed:
            self.center_y += self.speed * delta_time
            moving = True
            self.direction = "up"
        if arcade.key.S in self.keys_pressed:
            self.center_y -= self.speed * delta_time
            moving = True
            self.direction = "down"

        if arcade.key.D in self.keys_pressed:
            self.center_x += self.speed * delta_time
            moving = True
            self.direction = "right"
        if arcade.key.A in self.keys_pressed:
            self.center_x -= self.speed * delta_time
            moving = True
            self.direction = "left"

        if arcade.key.UP in self.keys_pressed and self.shoot_timer <= 0:
            arcade.play_sound(self.shot_sound)
            if self.double_barreled:
                bullet = Bullet("up")
                bullet.center_x = self.center_x - 10
                bullet.center_y = self.center_y
                bullets.append(bullet)

                bullet2 = Bullet('up')
                bullet2.center_x = self.center_x + 10
                bullet2.center_y = self.center_y
                bullets.append(bullet2)
            else:
                bullet = Bullet("up")
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y
                bullets.append(bullet)

            self.shoot_timer = self.shoot_cooldown
        if arcade.key.DOWN in self.keys_pressed and self.shoot_timer <= 0:
            arcade.play_sound(self.shot_sound)
            if self.double_barreled:
                bullet2 = Bullet('down')
                bullet2.center_x = self.center_x - 10
                bullet2.center_y = self.center_y
                bullets.append(bullet2)

                bullet = Bullet("down")
                bullet.center_x = self.center_x + 10
                bullet.center_y = self.center_y
                bullets.append(bullet)
            else:
                bullet = Bullet("down")
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y
                bullets.append(bullet)

            self.shoot_timer = self.shoot_cooldown
        if arcade.key.RIGHT in self.keys_pressed and self.shoot_timer <= 0:
            arcade.play_sound(self.shot_sound)
            if self.double_barreled:
                bullet2 = Bullet('right')
                bullet2.center_x = self.center_x
                bullet2.center_y = self.center_y + 10
                bullets.append(bullet2)

                bullet = Bullet("right")
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y - 10
                bullets.append(bullet)
            else:
                bullet = Bullet("right")
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y
                bullets.append(bullet)

            self.shoot_timer = self.shoot_cooldown
        if arcade.key.LEFT in self.keys_pressed and self.shoot_timer <= 0:
            arcade.play_sound(self.shot_sound)
            if self.double_barreled:
                bullet2 = Bullet('left')
                bullet2.center_x = self.center_x
                bullet2.center_y = self.center_y - 10
                bullets.append(bullet2)

                bullet = Bullet("left")
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y + 10
                bullets.append(bullet)
            else:
                bullet = Bullet("left")
                bullet.center_x = self.center_x
                bullet.center_y = self.center_y
                bullets.append(bullet)

            self.shoot_timer = self.shoot_cooldown

        if self.auto:
            if self.auto_timer == 0:  # чтобы при подборе сразу вылетали пули
                arcade.play_sound(self.shot2_sound)
                self.auto_timer += delta_time
                a_bullet1 = Bullet('up')
                a_bullet1.center_x = self.center_x
                a_bullet1.center_y = self.center_y
                bullets.append(a_bullet1)

                a_bullet2 = Bullet('right')
                a_bullet2.center_x = self.center_x
                a_bullet2.center_y = self.center_y
                bullets.append(a_bullet2)

                a_bullet3 = Bullet('down')
                a_bullet3.center_x = self.center_x
                a_bullet3.center_y = self.center_y
                bullets.append(a_bullet3)

                a_bullet4 = Bullet('left')
                a_bullet4.center_x = self.center_x
                a_bullet4.center_y = self.center_y
                bullets.append(a_bullet4)

            elif self.auto_timer < self.auto_cooldown:
                self.auto_timer += delta_time
                if self.auto_timer >= self.auto_cooldown:
                    self.auto_timer = 0.1
                    arcade.play_sound(self.shot2_sound)
                    a_bullet1 = Bullet('up')
                    a_bullet1.center_x = self.center_x
                    a_bullet1.center_y = self.center_y
                    bullets.append(a_bullet1)

                    a_bullet2 = Bullet('right')
                    a_bullet2.center_x = self.center_x
                    a_bullet2.center_y = self.center_y
                    bullets.append(a_bullet2)

                    a_bullet3 = Bullet('down')
                    a_bullet3.center_x = self.center_x
                    a_bullet3.center_y = self.center_y
                    bullets.append(a_bullet3)

                    a_bullet4 = Bullet('left')
                    a_bullet4.center_x = self.center_x
                    a_bullet4.center_y = self.center_y
                    bullets.append(a_bullet4)

        # не дает пройти персонажу за окно
        # if self.center_x <= 0:
        #     self.center_x = 0
        # if self.center_x >= SCREEN_WIDTH:
        #     self.center_x = SCREEN_WIDTH
        # if self.center_y <= 0:
        #     self.center_y = 0
        # if self.center_y >= SCREEN_HEIGHT:
        #     self.center_y = SCREEN_HEIGHT

        if moving:
            self.animation_timer += 1

            if self.animation_timer % 8 == 0:
                self.current_texture += 1
                if self.current_texture >= len(self.walk_down):
                    self.current_texture = 0

                if self.direction == "down":
                    self.texture = self.walk_down[self.current_texture]
                elif self.direction == "up":
                    self.texture = self.walk_up[self.current_texture]
                elif self.direction == "right":
                    self.texture = self.walk_right[self.current_texture]
                elif self.direction == "left":
                    self.texture = self.walk_left[self.current_texture]
        else:
            if self.direction == "down":
                self.texture = self.walk_down[0]
            elif self.direction == "up":
                self.texture = self.walk_up[0]
            elif self.direction == "right":
                self.texture = self.walk_right[0]
            elif self.direction == "left":
                self.texture = self.walk_left[0]

        # обновление баффов
        if self.speed_buff_timer > 0:
            self.speed_buff_timer -= delta_time
            if self.speed_buff_timer <= 0:
                self.speed = 200

        if self.double_buff_timer > 0:
            self.double_buff_timer -= delta_time
            if self.double_buff_timer <= 0:
                self.double_barreled = False

        if self.shoot_speed_buff_timer > 0:
            self.shoot_speed_buff_timer -= delta_time
            if self.shoot_speed_buff_timer <= 0:
                self.shoot_cooldown = 0.5

        if self.auto_buff_timer > 0:
            self.auto_buff_timer -= delta_time
            if self.auto_buff_timer <= 0:
                self.auto = False