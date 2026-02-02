import arcade
from utils import resource_path


class Bullet(arcade.Sprite):
    def __init__(self, direction):
        super().__init__()

        self.texture = arcade.load_texture(resource_path("assets/bullet.png"))
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
