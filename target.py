import arcade
from math import *
WIDTH = 800
HEIGHT = 800
TITLE = "game"

class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
        self.angle = 0

    def setup(self):
        self.coin = arcade.Sprite(':resources:images/items/coinGold.png')
        self.player = arcade.Sprite(':resources:images/animated_characters/zombie/zombie_idle.png')
        self.player.center_x = 100
        self.player.center_y = 100
        self.coin.center_x = WIDTH/2 + 300
        self.coin.center_y = HEIGHT/2 + 0

    def update(self, delta_time):
        diff_y =self.coin.center_y - self.player.center_y
        diff_x =self.coin.center_x - self.player.center_x
        angle = atan2(diff_y, diff_x)
        self.player.angle = degrees(angle)
        self.player.change_x = 5 * cos(angle)
        self.player.change_y = 5 * sin(angle)
        self.player.update()

    def on_draw(self):
        arcade.start_render
        self.coin.draw()
        self.player.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.coin.center_x = x
        self.coin.center_y = y

game = Game()
game.setup()
arcade.run

