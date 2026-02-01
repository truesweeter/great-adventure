import arcade
from config import *


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.ui_camera = arcade.camera.Camera2D()

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        self.ui_camera.use()
        self.keys_pressed = set()

        arcade.draw_rect_filled(
            arcade.rect.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            (0, 0, 0, 160)
        )

        arcade.draw_text(
            "ПАУЗА",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 30,
            arcade.color.WHITE,
            40,
            anchor_x="center",
            font_name="Minecraft Rus"
        )

    def on_key_release(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)