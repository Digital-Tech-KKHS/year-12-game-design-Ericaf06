import arcade
import math
from math import *
import random

WIDTH = 1200
HEIGHT = 900
TITLE = "platform"
PLAYER_MOVEMENT_SPEED = 9
PLAYER_JUMP_SPEED = 5
TILE_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING )
GRAVITY = 1
JUMP_SPEED = 30
LEFT_FACING = 1
RIGHT_FACING = 0
BULLET_SPEED = 20

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__()
        self.setup()
        self.tile_map = None
        self.bullet_list = None
        self.score = 0
        self.game_over_sound = arcade.load_sound(':resources:sounds/hurt3.wav')
        self.bullet = arcade.Sprite(':resources:images/space_shooter/laserBlue01.png')
        self.enemy = arcade.Sprite(':resources:images/space_shooter/meteorGrey_big4.png')
        self.enemy_2 = arcade.Sprite(':resources:images/space_shooter/meteorGrey_big2.png')
        self.boss = arcade.Sprite(':resources:images/tiles/mushroomRed.png')
        self.health = arcade.Sprite(':resources:images/space_shooter/playerLife1_green.png')
        self.boss_health = arcade.Sprite(':resources:images/tiles/mushroomRed.png')
        


    def setup(self):
        arcade.set_background_color(arcade.color.CEIL)
        layer_options = {
                'Ground': {
                    "use_spatial_hash": True
                }
            }
       
        self.tile_map = arcade.load_tilemap('./square.tmx', layer_options=layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list('player')
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()
        self.boss_health_list = arcade.SpriteList()
        self.boss = arcade.Sprite()
        self.enemy_2_list = arcade.SpriteList()
        self.score = 0
        self.player = Player()
        self.scene['player'].append(self.player)
        self.climbing_sound = arcade.load_sound(':resources:sounds/upgrade4.wav')
        self.coin_sound = arcade.load_sound(':resources:sounds/coin1.wav')
        self.jump_sound = arcade.load_sound(':resources:sounds/jump1.wav')
        self.kill_sound = arcade.load_sound(':resources:sounds/hurt3.wav')
        self.bullet_sound = arcade.load_sound(':resources:sounds/laser3.wav')
        self.game_over_sound = arcade.load_sound(':resources:sounds/jump5.wav')
        self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player,
                ladders = self.scene['Ladders'],
                walls = self.scene['Ground'],
                gravity_constant=GRAVITY
        )

        self.camera = arcade.Camera(WIDTH, HEIGHT)
        self.HUD_camera = arcade.Camera(WIDTH, HEIGHT)
        for i in range(5):
            self.health = arcade.Sprite(":resources:images/space_shooter/playerLife1_green.png")
            self.health.center_x = 50 + 40 * i
            self.health.center_y = HEIGHT - 100
            self.health_list.append(self.health)

        for i in range (5):
            self.boss_health = arcade.Sprite(':resources:images/tiles/mushroomRed.png')
            self.boss_health.center_x = 60 + 40 * i
            self.boss_health.center_y = HEIGHT -100
            self.boss_health_list.append(self.boss_health)



    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.enemy_2_list.draw()
        self.boss.draw()
        self.HUD_camera.use()
        arcade.draw_text(str(self.score), 15, HEIGHT - 50, arcade.color.BLACK, font_size = 50)
        arcade.draw_text(str(self.health_list), 15, HEIGHT - 50, arcade.color.BLACK, font_size = 50)
        arcade.draw_text(str(self.boss_health_list), 15, HEIGHT - 50, arcade.color.BLACK, font_size = 50)
        self.health_list.draw()
        self.boss_health_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        bullet = arcade.Sprite(':resources:images/space_shooter/laserBlue01.png')
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
        self.bullet_list.update()
        self.physics_engine.update()
        self.player.update_animation()
        camera_x = self.player.center_x - WIDTH / 2
        camera_y = self.player.center_y - HEIGHT / 2

        if camera_x < 0:
            camera_x = 0

        if camera_y < 15:
            camera_y = 15
        self.camera.move_to((camera_x, camera_y))

        spikes = arcade.check_for_collision_with_list(self.player, self.scene['Do Not Touch'])
       
        if spikes:
            self.player.center_x = 400
            self.player.center_y = 400
            self.health_list.pop()
            arcade.play_sound(self.kill_sound)
            if len(self.health_list) <= 0:
                self.player.kill()
                arcade.play_sound(self.game_over_sound)
                self.window.show_view(self.window.game_over)

        if random.random() < 0.01:
            self.enemy = arcade.Sprite(':resources:images/space_shooter/meteorGrey_big4.png')
            self.enemy.center_x = 500
            self.enemy.center_y = 300
            self.enemy_list.append(self.enemy)
        for self.enemy in self.enemy_list:
            self.enemy.center_x -=2

        if random.random() < 0.01:
            self.enemy_2 = arcade.Sprite(':resources:images/space_shooter/meteorGrey_big4.png')
            self.enemy_2.center_x = 500
            self.enemy_2.center_y = 600
            self.enemy_2_list.append(self.enemy_2)
        for self.enemy_2 in self.enemy_2_list:
            self.enemy_2.center_y -=2
       
        enemy_collisions = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        if len(enemy_collisions) > 0:
              self.player.kill()
              arcade.play_sound(self.game_over_sound)
              self.window.show_view(self.view.game_over)

        enemy_2_collisions = arcade.check_for_collision_with_list(self.player, self.enemy_2_list)
        if len(enemy_2_collisions) > 0:
              self.player.kill()
              arcade.play_sound(self.game_over_sound)
              self.window.show_view(self.view.game_over)
        
       
        for self.bullet in self.bullet_list:
            enemy_bullet = arcade.check_for_collision_with_list(self.bullet, self.enemy_list)
            if len(enemy_bullet) > 0:
                self.bullet.kill
                enemy_bullet[0].kill()

        for self.bullet in self.bullet_list:
            enemy_2_bullet = arcade.check_for_collision_with_list(self.bullet, self.enemy_2_list)
            if len(enemy_2_bullet) > 0:
                self.bullet.kill
                enemy_2_bullet[0].kill()

        if self.bullet.center_x >1000 or self.bullet.center_y < 0:
            self.bullet.kill()

        coins = arcade.check_for_collision_with_list(self.player, self.scene['Coins'])
        for coin in coins:
            self.score += 1
            coin.kill()
            

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.D:
            self.player.change_x  = PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.A:
            self.player.change_x  = -PLAYER_MOVEMENT_SPEED
        if symbol == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif symbol == arcade.key.E:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = PLAYER_MOVEMENT_SPEED
                arcade.play_sound(self.climbing_sound)

        if symbol == arcade.key.X:
            self.health_list.pop()
            if len(self.health_list) <= 0:
                self.player.kill()

    def on_key_release(self, symbol: int, modifiers: int):
        print(symbol, modifiers)
        if symbol == arcade.key.D:
            self.player.change_x  = 0
        if symbol == arcade.key.A:
            self.player.change_x  = 0
        elif symbol == arcade.key.E:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = 0

class Boss(arcade.Sprite):
    def __init__(self):
        super().__init__('spongey.png')
        self.center_x = 600
        self.center_y = 400

    def enemy_update_anitmation(self):

        super().__init__(':resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png')
        self.boss_center_x = 600
        self.boss_center_y = 400
        self.boss_idle_textures = load_texture_pair(':resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png')
        self.boss_walk_textures = []
        for i in range(2):
            boss_frames = load_texture_pair(':resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png')
            self.boss_walk_textures.append(boss_frames)


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(':resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png')
        self.center_x = 400
        self.center_y = 400
        self.idle_textures = load_texture_pair(':resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png')
        self.walk_textures = []
        for i in range(2):
            frames = load_texture_pair(f':resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png')
            self.walk_textures.append(frames)
        self.fall_textures = load_texture_pair(':resources:images/animated_characters/male_adventurer/maleAdventurer_fall.png')
        self.jump_textures = load_texture_pair(':resources:images/animated_characters/male_adventurer/maleAdventurer_jump.png')
        self.climb_textures = load_texture_pair(':resources:images/animated_characters/male_adventurer/maleAdventurer_climb0.png')
        self.face_direction = RIGHT_FACING
        self.walk_index = 0
        self.odo = 0

    def update_animation(self):
        if self.odo < 2:
            self.odo += 1
            return
        self.odo = 0
       
        if self.change_x > 0:
            self.face_direction = RIGHT_FACING
        if self.change_x < 0:
            self.face_direction = LEFT_FACING
       
        if self.change_y > 0:
            self.texture = self.jump_textures[self.face_direction]
            return
        if self.change_y > 0:
            self.texture = self.climb_textures[self.face_direction]
            return
        if self.change_y < 0:
            self.texture = self.fall_textures[self.face_direction]
            return
   
        if self.change_x != 0:
            self.walk_index += 1
            self.walk_index = self.walk_index % 2
            self.texture = self.walk_textures[self.walk_index][self.face_direction]
            return

        self.texture = self.idle_textures[self.face_direction]

def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)    ]

class WelcomeView(arcade.View):
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
            self.window.show_view(self.window.game_view)
       

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

        
    def on_draw(self):
        self.clear()
        arcade.draw_text("dead", 200, 400)
   
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            self.window.show_view(self.window.welcome_view)

class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH,HEIGHT,TITLE)
        self.game_view = MyGame()
        self.welcome_view = WelcomeView()
        self.game_over = GameOverView()
        self.show_view(self.welcome_view)

def main():
    window = MyGame()
    welcome_view = WelcomeView()
    game_over = GameOverView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
