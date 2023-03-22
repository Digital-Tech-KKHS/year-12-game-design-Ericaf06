import arcade

WIDTH = 1200
HEIGHT = 900
TITLE = "platform"
PLAYER_MOVEMENT_SPEED = 8
GRAVITY = 1
JUMP_SPEED = 30
LEFT_FACING = 1
RIGHT_FACING = 0

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

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.setup()
        self.tile_map = None

    def setup(self):
        arcade.set_background_color(arcade.color.CEIL)
        layer_options = {
                'Ground': {
                    "use_spatial_hash": True
                }
            }
        

        self.tile_map = arcade.load_tilemap('./Ground.tmx', layer_options=layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list('player')

        if self.reset_score:
           self.score = 0
        self.reset_score = True

        self.player = Player()
        self.scene['player'].append(self.player)
        self.coin_sound = arcade.load_sound(':resources:sounds/coin1.wav')
        self.jump_sound = arcade.load_sound(':resources:sounds/jump1.wav')
        self.kill_sound = arcade.load_sound(':resources:sounds/hurt3.wav')
        self.game_over_sound = arcade.load_sound(':resources:sounds/jump5.wav')
        self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player,
                self.scene['Ground'],
                ladders = self.scene['Ladders'],
                gravity_constant=GRAVITY
        )

        self.camera = arcade.Camera(WIDTH, HEIGHT)
        self.HUD_camera = arcade.Camera(WIDTH, HEIGHT)
        self.health_list = arcade.SpriteList()
        for i in range(5):
            health = arcade.Sprite(":resources:images/space_shooter/playerLife1_green.png")
            health.center_x = 50 + 40 * i
            health.center_y = HEIGHT - 100
            self.health_list.append(health)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

        self.HUD_camera.use()
        arcade.draw_text(str(self.score), 15, HEIGHT - 50, font_size=50)
        self.health_list.draw()

    def on_update(self, dt):
        self.physics_engine.update()
        self.player.update_animation()
        camera_x = self.player.center_x - WIDTH / 2
        camera_y = self.player.center_y - HEIGHT / 2

        if camera_x < 0:
            camera_x = 0

        if camera_y < 15:
            camera_y = 15
        self.camera.move_to((camera_x, camera_y))

        coins = arcade.check_for_collision_with_list(self.player, self.scene['Coins'])
        for coin in coins:
            self.score += 1
            coin.kill()
            arcade.play_sound(self.coin_sound)

        spikes = arcade.check_for_collision_with_list(self.player, self.scene['Do not touch'])

        if self.player.center_x >= self.end_of_map:
            self.level += 1
            self.reset_score = False
            self.setup()

        if spikes:
            self.player.center_x = 400
            self.player.center_y = 400
            self.health_list.pop()
            arcade.play_sound(self.kill_sound)
            if len(self.health_list) <= 0:
                self.player.kill()
                arcade.play_sound(self.game_over_sound)
                self.window.show_view(self.window.game_over)



    def on_key_press(self, symbol: int, modifiers: int):
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

    def on_show(self):
        arcade.set_background_color(arcade.color.GENERIC_VIRIDIAN)

class WelcomeView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AFRICAN_VIOLET)
   
    def on_draw(self):
        self.clear()
        arcade.draw_text("Feeling devious? press enter", 200, 400)
   
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            self.window.show_view(self.window.game_view)

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AFRICAN_VIOLET)
   
    def on_draw(self):
        self.clear()
        arcade.draw_text("dead", 200, 400)
   
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            self.window.show_view(self.window.welcome_view)

class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH,HEIGHT,TITLE)
        self.game_view = GameView()
        self.welcome_view = WelcomeView()
        self.game_over = GameOverView()
        self.show_view(self.welcome_view)

game = Game()
arcade.run()

