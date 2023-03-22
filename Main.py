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