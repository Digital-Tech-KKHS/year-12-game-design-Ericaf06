import arcade
import random

WIDTH = 800
HEIGHT = 800
TITLE = "lasers"

PLAYER_SCALING = 0.8
COIN_SCALING = 0.3
LAZER_SCALING = 0.5
BULLET_SPEED = 15

class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        self.player = None
        self.coint_list = None
        self.bullet_list = None

        self.score = 0 
        self.set_mouse_visible = (False)
        self.coin_sound = arcade.load_sound(':resources:sounds/coin1.wav')
        self.laser_sound = arcade.load_sound(':resources:sounds/laser3.wav')
   
    def setup(self):
        self.player = arcade.Sprite(":resources:images/space_shooter/playerShip1_blue.png")
        self.player.center_y = 200
        self.player.center_x = WIDTH/2
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.score = 0
        arcade.set_background_color(arcade.color.AMAZON)
        for i in range(80):
            coin = arcade.Sprite(':resources:images/space_shooter/meteorGrey_med2.png')
            coin.center_x = random.randint(0, WIDTH)
            coin.center_y = random.randint(250, HEIGHT)
            self.coin_list.append(coin)

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.coin_list.draw()
        self.bullet_list.draw()
        arcade.draw_text(f" Score: {self.score}", 20, HEIGHT -20,  arcade.color.WHITE)
   
    def update(self, delta_time):
        self.bullet_list.update()
        for bullet in self.bullet_list:
            touching = arcade.check_for_collision_with_list(bullet, self.coin_list)
            for coin in touching:
                coin.kill()
                self.score += 1
                arcade.play_sound(self.coin_sound)

   

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.center_x = x
   
    def on_mouse_press(self, x, y, button, modifiers):
        bullet = arcade.Sprite(':resources:images/space_shooter/laserBlue01.png')
        bullet.center_x = x
        bullet.center_y = self.player.center_y
        bullet.change_y = BULLET_SPEED
        bullet.angle = 90
        self.bullet_list.append(bullet)
        arcade.play_sound(self.laser_sound)

   

game = Game()
game.setup()
arcade.run()