import arcade

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
            bullet = Bullet("up")
            bullet.center_x = self.center_x
            bullet.center_y = self.center_y
            bullets.append(bullet)
            
            self.shoot_timer = self.shoot_cooldown
        if arcade.key.DOWN in self.keys_pressed and self.shoot_timer <= 0:
            bullet = Bullet("down")
            bullet.center_x = self.center_x
            bullet.center_y = self.center_y
            bullets.append(bullet)

            self.shoot_timer = self.shoot_cooldown
        if arcade.key.RIGHT in self.keys_pressed and self.shoot_timer <= 0:
            bullet = Bullet("right")
            bullet.center_x = self.center_x
            bullet.center_y = self.center_y
            bullets.append(bullet)
            self.shoot_timer = self.shoot_cooldown
        if arcade.key.LEFT in self.keys_pressed and self.shoot_timer <= 0:
            bullet = Bullet("left")
            bullet.center_x = self.center_x
            bullet.center_y = self.center_y
            bullets.append(bullet)
            self.shoot_timer = self.shoot_cooldown
        



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

        


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)

        self.player_list = arcade.SpriteList()
        self.player = Hero()
        self.player_list.append(self.player)

        self.bullets = arcade.SpriteList()
        

    def setup(self):
        self.keys_pressed = set()

    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.bullets.draw()

    def on_update(self, delta_time):
        self.player.update(self.keys_pressed, delta_time, self.bullets)
        self.bullets.update(delta_time)

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        
    def on_key_release(self, key, modifiers):
        self.keys_pressed.remove(key)

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()  # Запускаем начальную настройку игры
    arcade.run()


if __name__ == "__main__":
    main()