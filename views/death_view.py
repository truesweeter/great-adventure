import arcade
import json
import os

from config import *
from utils import resource_path, get_writable_path


class DeathView(arcade.View):
    def __init__(self, kills_count, time_survived):
        super().__init__()
        self.time_survived = time_survived
        self.kills_count = kills_count
        skull = arcade.Sprite(resource_path("assets/skull.png"))
        skull.center_x = SCREEN_WIDTH / 2
        skull.center_y = SCREEN_HEIGHT / 2 + 100
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(skull)
        arcade.set_background_color(arcade.color.GRAY_BLUE)
        self.keys_pressed = []

        self.arrow_y = [SCREEN_HEIGHT / 2 - 170, SCREEN_HEIGHT / 2 - 220]
        self.arrow_pick = "UP"
        self.arrow = arcade.Sprite(resource_path("assets/arrow.png"))
        self.arrow.scale = 0.35
        self.arrow.center_x = SCREEN_WIDTH / 2 - 30
        self.arrow.center_y = SCREEN_HEIGHT / 2 - 175
        self.all_sprites.append(self.arrow)

        self.ui_camera = arcade.camera.Camera2D()
        self.death_sound = arcade.load_sound(
            resource_path("assets/sounds/lose.wav")
        )
        self.select_sound = arcade.load_sound(
            resource_path("assets/sounds/select.wav")
        )
        self.start_sound = arcade.load_sound(
            resource_path("assets/sounds/start.wav")
        )
        arcade.play_sound(self.death_sound)

        self.new_record = False
        max_kills = 0
        max_time = 0
        try:
            with open(get_writable_path("data/records.json"),
                      "r", encoding="utf-8") as f:
                data = json.load(f)
                max_kills = data["max_kills"]
                max_time = data["max_time"]
        except Exception:
            max_kills = 0
            max_time = 0
        print(max_kills, max_time)
        if self.kills_count > max_kills:
            max_kills = self.kills_count
            self.new_record = True
        if self.time_survived > max_time:
            max_time = int(self.time_survived)
            self.new_record = True

        path = get_writable_path("data/records.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        record = {"max_kills": max_kills, "max_time": max_time}
        with open(get_writable_path("data/records.json"),
                  mode="w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=4)

    def on_draw(self):
        self.clear()
        self.ui_camera.use()
        self.all_sprites.draw()
        arcade.draw_text("Вы умерли! Желаете начать заново?",
                         SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 100,
                         font_name="Minecraft Rus", font_size=17)

        arcade.draw_text("Да, начать новую игру", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 175,
                         font_name="Minecraft Rus", font_size=15)
        arcade.draw_text("Нет, выйти из игры", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 225,
                         font_name="Minecraft Rus", font_size=15)
        arcade.draw_text(
            f"Убийства: {self.kills_count}",
            SCREEN_WIDTH // 2 - 250,
            SCREEN_HEIGHT // 2 - 175,
            arcade.color.WHITE,
            15,
            font_name="Minecraft Rus"
        )

        arcade.draw_text(
            f"Время: {int(self.time_survived)} c",
            SCREEN_WIDTH // 2 - 250,
            SCREEN_HEIGHT // 2 - 225,
            arcade.color.WHITE,
            15,
            font_name="Minecraft Rus"
        )

        if self.new_record:
            arcade.draw_text(
                "НОВЫЙ РЕКОРД",
                SCREEN_WIDTH / 2 - 122,
                SCREEN_HEIGHT / 2 + 250,
                arcade.color.YELLOW,
                20,
                font_name="Minecraft Rus"
            )

        with open(get_writable_path("data/records.json"),
                  "r", encoding="utf-8") as f:
            data = json.load(f)
            max_kills = data["max_kills"]
            max_time = data["max_time"]

        arcade.draw_text(
            f"Рекорд убийств: {max_kills}",
            30,
            50,
            arcade.color.WHITE,
            14,
            font_name="Minecraft Rus"
        )
        arcade.draw_text(
            f"Рекорд по времени: {max_time} c",
            30,
            25,
            arcade.color.WHITE,
            14,
            font_name="Minecraft Rus"
        )

    def on_update(self, delta_time):
        if arcade.key.UP in self.keys_pressed:
            if self.arrow_pick == "DOWN":
                arcade.play_sound(self.select_sound)
            self.arrow_pick = "UP"

        if arcade.key.DOWN in self.keys_pressed:
            if self.arrow_pick == "UP":
                arcade.play_sound(self.select_sound)
            self.arrow_pick = "DOWN"

        if self.arrow_pick == "UP":
            self.arrow.center_y = self.arrow_y[0]
        elif self.arrow_pick == "DOWN":
            self.arrow.center_y = self.arrow_y[1]

        if arcade.key.ENTER in self.keys_pressed:
            if self.arrow_pick == "UP":
                arcade.play_sound(self.start_sound)
                from views.game_view import GameView
                self.window.show_view(GameView())
            elif self.arrow_pick == "DOWN":
                arcade.exit()

    def on_key_press(self, key, modifiers):
        self.keys_pressed.append(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
