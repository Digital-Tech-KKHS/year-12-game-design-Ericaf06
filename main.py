"""Imports"""
import arcade
import math
from math import atan2, degrees
import pathlib

"""Global variables"""
PARENT_DIR = pathlib.Path(__file__).parent
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1200
TITLE = "platform"
PLAYER_MOVEMENT_SPEED = 13
PLAYER_JUMP_SPEED = 4
TILE_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)
GRAVITY = 1
JUMP_SPEED = 30
LEFT_FACING = 1
RIGHT_FACING = 0
BULLET_SPEED = 20
BOSS_SPEED = 10

    
class MyGame(arcade.Window):
    """Game class"""

    def __init__(self):
        super().__init__()
        self.setup()
        self.tile_map = None
        self.score = 0
        self.level = 1
        self.camera = None
        #Loads Mp3 sounds used in game
        self.game_over_sound = arcade.load_sound(
            'lose_sound.mp3'
        )
        self.game_win_sound = arcade.load_sound(
            'win_sound.mp3'
        )
        self.climbing_sound = arcade.load_sound(
            'climbing_sound.mp3'
        )
        self.coin_sound = arcade.load_sound(
            'coin_sound.mp3'
        )
        self.jump_sound = arcade.load_sound(
            'jump_sound.mp3'
        )
        self.kill_sound = arcade.load_sound(
            'ouch_sound (3).mp3'
        )
        self.bullet_sound = arcade.load_sound(
            'bullet_sound.mp3'
        )
        self.bullet = arcade.Sprite(
            PARENT_DIR/ 'Bullet-0006.png'
        )
      
        
    def setup(self):
        """Set up function for game, loads scene, map and, sprites"""
        
        arcade.set_background_color(arcade.color.CEIL)
        layer_options = {
            'Ground': {
                "use_spatial_hash": True
            }
        }
        self.level = 1
        #Loads in tile map and adds scene from tile map
        self.tile_map = arcade.load_tilemap(
            './Level_1.tmx', layer_options=layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        #Creates bullet list and adds to scene
        #Adds player to scene by referencing player class
        self.bullet_list = arcade.SpriteList()
        self.scene.add_sprite_list(
            'bullets',sprite_list=self.bullet_list
        )
        self.player = Player()
        self.scene.add_sprite_list(
            'player',sprite_list = self.player
            )
        #Creates physics engine, allows game to follow laws of physics
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.scene['Ground'], 
            ladders=self.scene['Ladders'],
            platforms=self.scene['Moving'],
            gravity_constant=GRAVITY,
        )
        #Creates cameras 
        self.camera = arcade.Camera(self.width, self.height
            )
        #self.HUD_camera = arcade.Camera(
           # SCREEN_WIDTH, SCREEN_HEIGHT
           # )
        #Creates health list and adds to scene
        self.health = 5
        self.health_list = arcade.SpriteList()
        for i in range(5):
            health = arcade.Sprite(
                PARENT_DIR/ 'Health-0008.png'
                )
            health.center_x = 35 + 40 * i
            health.center_y = SCREEN_HEIGHT - 100
            self.health_list.append(health)
        
    def on_draw(self):
        """Draws lists and text"""

        self.clear()
        self.camera.use()
        self.bullet_list.draw()
        #self.health_list.draw()
        self.scene.draw()
        #self.HUD_camera.use()
        #Draws the score text
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.BLACK,
            20,
        )
        #Draws texts explaining to the user how to move the player
        w_text ='W key: Jump'
        arcade.draw_text(
            w_text,
            20,
            570,
            arcade.csscolor.BLACK,
            10
        )
        a_text = 'A key: Right'
        arcade.draw_text(
            a_text,
            20,
            555,
            arcade.csscolor.BLACK,
            10
        )
        d_text = 'D key: Left'
        arcade.draw_text(
            d_text,
            20,
            540,
            arcade.csscolor.BLACK,
            10
        )
        e_text = 'E key: Climb ladders'
        arcade.draw_text(
            e_text,
            20,
            525,
            arcade.csscolor.BLACK,
            10
        )
        shoot_text = 'Mouse click: Shoot bullets'
        arcade.draw_text(
            shoot_text,
            20,
            510,
            arcade.csscolor.BLACK,
            10
        )

    def player_camera(self, x, y):
        """Takes coordinates of player and screen
        Which allows camera to centre on the player"""
        #Camera code sourced from Python arcade library step 6- Adding a camera

        screen_center_x = self.player.center_x - (
            self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)
        
    def on_mouse_press(self, x, y, button, modifiers):
        """Called when mouse is pressed"""

        bullet = arcade.Sprite(
            PARENT_DIR/'Bullet-0006.png'
        )
        #Ensures bullet spawns from players x,y coordinates
        #Takes difference between x,y and start x,y
        #Using atan2, the difference taken allows bullet
        #To move in any direction the mouses' x and y are
        #https://www.youtube.com/watch?v=m2aQEBAaKic
        start_x = self.player.center_x
        start_y = self.player.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y
        arcade.play_sound(self.bullet_sound)
        dest_x = x
        dest_y = y
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)
        bullet.angle = math.degrees(angle)
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        self.bullet_list.append(bullet)

    def on_update(self, dt):
        """Updates scene"""
        self.bullet_list.update()
        self.physics_engine.update()
        self.player.update_animation()
        camera_x = self.player.center_x / 2
        camera_y = self.player.center_y / 2

        if camera_x < 0:
            camera_x = 0

        if camera_y < 20:
            camera_y = 20
        self.camera.move_to((camera_x, camera_y))
        
        self.center_camera__to_player()

        #Checks for colisions with plsyer and tile layer
        danger = arcade.check_for_collision_with_list(
            self.player, self.scene['Danger'])
        
        hurt = arcade.check_for_collision_with_list(
            self.player, self.scene['Hurt'])
        #If the player collides with the scene layer 
        #Stated in the hurt function, health will decrease by 1
        if hurt:
            self.player.center_x =400
            self.player.center_y = 400
            arcade.play_sound(self.kill_sound)
            self.health_list.pop()
            game_over = GameOverView
        if len(self.health_list) <= 0:
            self.player.kill()
            arcade.play_sound(self.game_over_sound)
            self.window.show_view(game_over)
        
        if danger:
            self.player.center_x = 400
            self.player.center_y = 400
            arcade.play_sound(self.kill_sound)
            self.health_list.pop()
            game_over = GameOverView()
        if len(self.health_list) <= 0:
            self.player.kill()
            arcade.play_sound(self.game_over_sound)
            self.window.show_view(game_over)
        
        #Kills bullet after it has travelled past these points
        #This helps the game from crashing if too many bullets are fired
        if self.bullet.center_x > 1000 or self.bullet.center_y < 0:
            self.bullet.kill()

        #If player collides with coins score increases by 1
        coins = arcade.check_for_collision_with_list(
            self.player, self.scene['Coins'])
        for coin in coins:
            self.score += 1
            coin.kill()
        if self.score == 10:
            self.level +1
        elif self.score == 10 and self.level >=3:
            game_win = GameWinView
            self.window.show_view(game_win)

        #Is able to shoot enemy and kill them with bullets 
        #https://www.youtube.com/watch?v=m2aQEBAaKic
        for self.bullet in self.bullet_list:
            enemy_bullet = arcade.check_for_collision_with_list(
                self.bullet, self.scene['Hurt'])
            if len(enemy_bullet) > 0:
                self.bullet.kill
                enemy_bullet[0].kill()

    def on_key_press(self, symbol, modifiers):
        """Called when key is pressed. Controls player movement"""
        if symbol == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        if symbol == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif symbol == arcade.key.E:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = PLAYER_MOVEMENT_SPEED
                arcade.play_sound(self.climbing_sound)
        elif symbol == arcade.key.Q:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = -PLAYER_MOVEMENT_SPEED

    def on_key_release(self, symbol, modifiers):
        """Called when key is released"""
        if symbol == arcade.key.D:
            self.player.change_x = 0
        if symbol == arcade.key.A:
            self.player.change_x = 0
        if symbol == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = 0
        elif symbol == arcade.key.E:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = 0
        elif symbol == arcade.key.Q:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = 0

        
class Player(arcade.Sprite):
    """Player class which manages players position, textures and movement"""

    def __init__(self):
        super().__init__(PARENT_DIR/'Fairy-0001.png'
            )
        self.center_x = 400
        self.center_y = 400
        self.face_direction = RIGHT_FACING
        self.walk_index = 0
        self.odo = 0

class WelcomeView(arcade.View):
    """View that shows when game is loaded"""

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AFRICAN_VIOLET)

    def on_show(self):
        arcade.set_background_color(arcade.color.AFRICAN_VIOLET)

    def on_draw(self):
        self.clear()
        arcade.draw_text(" you wanna play? press enter", 200, 400)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            game_view = MyGame()
            self.window.show_view(game_view)


class GameWinView(arcade.View):
    """View that shows when the player wins"""

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BRILLIANT_LAVENDER)

    
    def on_show(self):
        arcade.set_background_color(arcade.color.BRILLIANT_LAVENDER)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Congratulations you win!!. Press enter to play again.", 200, 400)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            welcome_view = WelcomeView()
            self.window.show_view(welcome_view)


class GameOverView(arcade.View):
    """View that shows when player dies/loses"""

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BULGARIAN_ROSE)

    def on_show(self):
        arcade.set_background_color(arcade.color.BULGARIAN_ROSE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("You couldn't save your friend in time. Press enter to play again", 200, 400)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            welcome_view = WelcomeView()
            self.window.show_view(welcome_view)


class Game(arcade.Window):
    """Manages different game views and windows"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
        self.game_view = MyGame()
        self.win_view = GameWinView()
        welcome_view = WelcomeView()
        self.game_over = GameOverView()
        self.window.show_view(welcome_view)

#Allows game to run 
def main():
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
