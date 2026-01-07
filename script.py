import arcade
import math 
import random


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Great Adventure"
SPRITE_SIZE = 32
FRAMES = 8

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
            arcade.load_texture("assets/hero/down0.png"),
            arcade.load_texture("assets/hero/down1.png"),
            arcade.load_texture("assets/hero/down2.png"),
            arcade.load_texture("assets/hero/down3.png")
        ]

        self.walk_up = [
            arcade.load_texture("assets/hero/up0.png"),
            arcade.load_texture("assets/hero/up1.png"),
            arcade.load_texture("assets/hero/up2.png"),
            arcade.load_texture("assets/hero/up3.png")
        ]

        self.walk_right = [
            arcade.load_texture("assets/hero/right0.png"),
            arcade.load_texture("assets/hero/right1.png"),
            arcade.load_texture("assets/hero/right2.png"),
            arcade.load_texture("assets/hero/right3.png")
        ]

        self.walk_left = [
            arcade.load_texture("assets/hero/left0.png"),
            arcade.load_texture("assets/hero/left1.png"),
            arcade.load_texture("assets/hero/left2.png"),
            arcade.load_texture("assets/hero/left3.png")
        ]

        self.current_texture = 0
        self.animation_timer = 0
        self.texture = self.walk_down[0]
        self.direction = "down"

        self.shoot_timer = 0
        self.shoot_cooldown = 0.5


    def get_buff(self, item):
        if item.buff == 'speed':
            self.speed = 275 # увеличение скорости игрока до 275
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
            if self.auto_timer == 0: # чтобы при подборе сразу вылетали пули
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

        #не дает пройти персонажу за окно
        if self.center_x <= 0:
            self.center_x = 0
        if self.center_x >= SCREEN_WIDTH:
            self.center_x = SCREEN_WIDTH
        if self.center_y <= 0:
            self.center_y = 0
        if self.center_y >= SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT
        

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

class Bullet(arcade.Sprite):
    def __init__(self, direction):
        super().__init__()

        self.texture = arcade.load_texture("assets/bullet.png")
        self.direction = direction
        self.speed = 500

    def update(self, delta_time):
        if self.direction == "right":
            self.center_x += self.speed * delta_time
        elif self.direction == "left":
            self.center_x -= self.speed * delta_time
        elif self.direction == "up":
            self.center_y += self.speed * delta_time
        elif self.direction == "down":
            self.center_y -= self.speed * delta_time

        if (
            self.right < 0 or
            self.left > SCREEN_WIDTH or
            self.top < 0 or
            self.bottom > SCREEN_HEIGHT
        ):
            self.remove_from_sprite_lists()

        
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
            arcade.load_texture("assets/enemy1/walk0.png"),
            arcade.load_texture("assets/enemy1/walk1.png"),
            arcade.load_texture("assets/enemy1/walk2.png"),
            arcade.load_texture("assets/enemy1/walk3.png")
        ]
        self.death_animation = [
            arcade.load_texture("assets/enemy1/death0.png"),
            arcade.load_texture("assets/enemy1/death1.png"),
            arcade.load_texture("assets/enemy1/death2.png"),
            arcade.load_texture("assets/enemy1/death3.png"),
            arcade.load_texture("assets/enemy1/death4.png"),
            arcade.load_texture("assets/enemy1/death5.png"),
            arcade.load_texture("assets/enemy1/death6.png"),
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


class Item(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 1
        self.speed = 30
        self.timer = 0
        self.direction = 1

    def update(self, delta_time):
        self.timer += delta_time
        self.center_y += self.direction * self.speed * delta_time
        if self.timer % 1 > 0.5:
            self.direction = 1
        else:
            self.direction = -1

class Pepper(Item):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('assets/items/pepper.png')
        self.buff = 'speed'

class DoubleBarreled(Item):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('assets/items/shotgun.png')
        self.scale = 1.3
        self.buff = 'double'

class DoublePistols(Item):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('assets/items/revolver.png')
        self.buff = 'shoot_speed'
        self.scale = 1.7

class Nuke(Item):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('assets/items/nuke.png')
        self.buff = 'nuke'
        self.scale = 1

class Autogun(Item):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('assets/items/auto-shotgun.png')
        self.buff = 'auto'

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.keys_pressed = []
        self.timer = 0

        self.player_list = arcade.SpriteList()
        self.player = Hero()
        self.player_list.append(self.player)

        self.bullets = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.items = arcade.SpriteList()

    def setup(self):
        self.keys_pressed = set()
        self.timer = 0

    def on_draw(self):
        self.clear()
        self.enemies.draw()
        self.player_list.draw()
        self.bullets.draw()
        self.items.draw()

    def on_update(self, delta_time):
        self.player.update(self.keys_pressed, delta_time, self.bullets)
        self.bullets.update(delta_time)
        self.enemies.update(delta_time)
        self.items.update(delta_time)

        #спавн жуков
        self.timer += delta_time
        if self.timer >= 1:
            spawn = random.choice([True, False, False, False]) #шанс на спавн 25%
            if spawn:
                self.timer = 0
                enemy = EnemyBeatle(self.player)
                position = random.randint(0, 1)
                if position == 0:
                    enemy.center_y = random.randint(0, SCREEN_HEIGHT)
                    enemy.center_x = random.choice([0, SCREEN_WIDTH])
                else:
                    enemy.center_x = random.randint(0, SCREEN_WIDTH)
                    enemy.center_y = random.choice([0, SCREEN_HEIGHT])
                self.enemies.append(enemy)
            else:
                pass
        
        #попадение выстрела в жука
        for bullet in self.bullets:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies)
            for enemy in hit_list:
                if not enemy.is_dead:
                    bullet.remove_from_sprite_lists()
                if not enemy.is_dead:
                    enemy.is_dead = True
                    enemy.animation_timer = 0
                    enemy.current_texture = 0
                    enemy.texture = enemy.death_animation[0]
                    # выпадение предметов с жуков
                    drop = random.choice(
                        [False, False, False, False, False, False, False, True] # шанс появления предмета 12,5%
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
                        if len(self.items) > 2: # максимум два предмета на карте
                            self.items[0].remove_from_sprite_lists()


        # подбор предмета
        picked_items = arcade.check_for_collision_with_list(self.player, self.items)
        for item in picked_items:
            item.remove_from_sprite_lists()
            self.player.get_buff(item)

            if item.buff == 'nuke': # подбор игроком ядерки
                for enemy in self.enemies:
                    if enemy.is_dead == False:
                        enemy.is_dead = True
                        enemy.animation_timer = 0
                        enemy.current_texture = 0
                        enemy.texture = enemy.death_animation[0]

        #смерть героя
        hit_list = arcade.check_for_collision_with_list(self.player, self.enemies)
        for enemy in hit_list:
            if not enemy.is_dead:
                death_view = DeathView()
                self.window.show_view(death_view)
                

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_key_press(self, key, modifiers):
        self.keys_pressed.append(key)
        
    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.keys_pressed = []
        self.logo_list = arcade.SpriteList()
        logo = arcade.Sprite("assets/logo.png")
        logo.scale = 0.3
        self.logo_list.append(logo)
        logo.center_x = SCREEN_WIDTH / 2
        logo.center_y = SCREEN_HEIGHT / 2 + 100
        arcade.set_background_color(arcade.color.BLACK)


    def on_draw(self):
        self.clear()
        self.logo_list.draw()
        arcade.draw_text("Для начала игры нажмите любую клавишу", SCREEN_WIDTH / 2 - 275, SCREEN_HEIGHT / 2 - 200, font_size=17, font_name="Minecraft Rus")

    def on_key_press(self, key, modifiers):
        self.keys_pressed.append(key)

    def on_update(self, delta_time):
        if self.keys_pressed:
            game_view = GameView()
            self.window.show_view(game_view)


class DeathView(arcade.View):
    def __init__(self):
        super().__init__()
        skull = arcade.Sprite("assets/skull.png")
        skull.center_x = SCREEN_WIDTH / 2
        skull.center_y = SCREEN_HEIGHT / 2 + 100
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(skull)
        arcade.set_background_color(arcade.color.GRAY_BLUE)
        self.keys_pressed = []

        #cтрелка выбора
        self.arrow_y = [SCREEN_HEIGHT / 2 - 170, SCREEN_HEIGHT / 2 - 220]
        self.arrow_pick = "UP"
        self.arrow = arcade.Sprite("assets/arrow.png")
        self.arrow.scale = 0.35
        self.arrow.center_x = SCREEN_WIDTH / 2 - 230
        self.arrow.center_y = SCREEN_HEIGHT / 2 - 175
        self.all_sprites.append(self.arrow)


    def on_draw(self):
        self.clear()
        self.all_sprites.draw()
        arcade.draw_text("Вы умерли! Желаете начать заново?", SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 100, font_name="Minecraft Rus", font_size=17)

        arcade.draw_text("Да, начать новую игру", SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 175, font_name="Minecraft Rus", font_size=15)
        arcade.draw_text("Нет, выйти из игры", SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 225, font_name="Minecraft Rus", font_size=15)

    def on_update(self, delta_time):
        if arcade.key.UP in self.keys_pressed:
            self.arrow_pick = "UP"
        if arcade.key.DOWN in self.keys_pressed:
            self.arrow_pick = "DOWN"

        if self.arrow_pick == "UP":
            self.arrow.center_y = self.arrow_y[0]
        elif self.arrow_pick == "DOWN":
            self.arrow.center_y = self.arrow_y[1]

        if arcade.key.ENTER in self.keys_pressed:
            if self.arrow_pick == "UP":
                game_view = GameView()
                self.window.show_view(game_view)
            elif self.arrow_pick == "DOWN":
                arcade.exit()

    def on_key_press(self, key, modifiers):
        self.keys_pressed.append(key)

    def on_key_release(self, key, modifiers):
        self.keys_pressed.remove(key)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.load_font("assets/fonts/PixelFont.ttf")
    arcade.run()



if __name__ == "__main__":
    main()