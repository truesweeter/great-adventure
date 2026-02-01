import arcade

from config import *
from views.start_view import StartView
from utils import resource_path


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.load_font(resource_path("assets/fonts/PixelFont.ttf"))

    start_view = StartView()
    window.show_view(start_view)

    arcade.run()


if __name__ == "__main__":
    main()
