import arcade
from config import *
from utils import resource_path
from views.game_view import GameView


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.keys_pressed = []
        self.logo_list = arcade.SpriteList()
        logo = arcade.Sprite(resource_path("assets/logo.png"))
        logo.scale = 0.3
        self.logo_list.append(logo)
        logo.center_x = SCREEN_WIDTH / 2
        logo.center_y = SCREEN_HEIGHT / 2 + 100
        arcade.set_background_color(arcade.color.BLACK)

        self.start_sound = arcade.load_sound(resource_path("assets/sounds/start.wav"))

    def on_draw(self):
        self.clear()
        self.logo_list.draw()
        arcade.draw_text("Для начала игры нажмите любую клавишу", SCREEN_WIDTH / 2 - 275, SCREEN_HEIGHT / 2 - 200,
                         font_size=17, font_name="Minecraft Rus")

    def on_key_press(self, key, modifiers):
        self.keys_pressed.append(key)

    def on_update(self, delta_time):
        if self.keys_pressed:
            game_view = GameView()
            arcade.play_sound(self.start_sound)
            self.window.show_view(game_view)