import arcade
from utils import resource_path


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
        self.texture = arcade.load_texture(resource_path('assets/items/pepper.png'))
        self.buff = 'speed'


class DoubleBarreled(Item):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(resource_path('assets/items/shotgun.png'))
        self.scale = 1.4
        self.buff = 'double'


class DoublePistols(Item):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(resource_path('assets/items/revolver.png'))
        self.buff = 'shoot_speed'


class Nuke(Item):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(resource_path('assets/items/nuke.png'))
        self.buff = 'nuke'
        self.scale = 1


class Autogun(Item):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(resource_path('assets/items/auto-shotgun.png'))
        self.buff = 'auto'



