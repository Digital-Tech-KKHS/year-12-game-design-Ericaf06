## Test 1: Collecting coins
Date: 3/4/2023

```python
  coins = arcade.check_for_collision_with_list(self.player, self.scene['Coins'])
        for coin in coins:
            self.score += 1
            coin.kill()
            arcade.play_sound(self.coin_sound)
```

| Test Data                    | Expected                        | Observed                       |
| ---------------------------- | ------------------------------- | ------------------------------ |
| Player not touching/colliding with a coin  | Nothing happens in terms of score| As expected |
| Player touching/colliding with a coin | Score to increase by 1| As expected |
| Player touching/colliding with multiple coins at a time  |Score increases with the amount of coins the player collided with| As expected |

## Test 2: Ladder logic
Date: 3/4/2023

```python
#Ladders in physics engine
 self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player,
                self.scene['Ground'],
                ladders = self.scene['Ladders'],
                gravity_constant=GRAVITY
 )
 #on_key_press
 elif symbol == arcade.key.E:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = PLAYER_MOVEMENT_SPEED
 #on_key_release
  elif symbol == arcade.key.E:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = 0
```

| Test Data                    | Expected                        | Observed                       |
| ---------------------------- | ------------------------------- | ------------------------------ |
| Player climbing up ladder   | Player smoothly moves up ladder with climbing texture ||
| Player climbing down ladder |Player smoothly moves down ladder with climbing texture | |
| Player standing still on ladder| Player is able to standing still facing the direction they were jumping to |As expected|


## Test 3: Shooting bullets
Date: 4/05/2023
```python

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

```

| Test Data                    | Expected                        | Observed                       |
| ---------------------------- | ------------------------------- | ------------------------------ |
|Mouse pressed to bottom left of player|  Bullet shoots to the bottom left of the player | As expected
|Player shooting in a horizontal line on a ladder| Bullet shoots out horizontally |Bullet doesn't shoot
|Mouse pressed in direction of enemy| Bullet shoots towards enemy | As expected |



## Test 4: Player Movement
Date: 8/05/2023
```python
def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.D:
            self.player.change_x  = PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.A:
            self.player.change_x  = -PLAYER_MOVEMENT_SPEED
        if symbol == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif symbol == arcade.key.E:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = PLAYER_MOVEMENT_SPEED
                arcade.play_sound(self.climbing_sound)
      
def on_key_release(self, symbol: int, modifiers: int):
        print(symbol, modifiers)
        if symbol == arcade.key.D:
            self.player.change_x  = 0
        if symbol == arcade.key.A:
            self.player.change_x  = 0
        elif symbol == arcade.key.E:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = 0


```

| Test Data                    | Expected                        | Observed                       |
| ---------------------------- | ------------------------------- | ------------------------------ |
|W pressed| Player jumps in place|As expected
|W pressed while D is pressed|Player Jumps foward|As expected
|E pressed while player is infront of ladder | Player moves up the ladder| As expected |

## Test 5: Spikes
Date: 09/05/2023
```python
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
```

| Test Data                    | Expected                        | Observed                       |
| ---------------------------- | ------------------------------- | ------------------------------ |
|Player lands on spikes layer | Health decreases by one and player restarts | As expected|
|Player misses spikes layer| Nothing happens to players health| As expected|
|Player lands on spikes twice| Players health decreases by 2 |As expected  |

## Test 6: Enemy Collisions
Date: 25/05/2023
```python
 for self.player in enemy_collisions:
            self.health -= 1
            self.player.kill()
            arcade.play_sound(self.kill_sound)
            game = MyGame()
            (game)
            if len(self.health_list) > 0:
                self.player.kill()
            arcade.play_sound(self.game_over_sound)
            game_over = GameOverView()
            (game_over)
```

| Test Data                    | Expected                        | Observed                       |
| ---------------------------- | ------------------------------- | ------------------------------ |
|Player collides with enemy| Player restarts on game with one less health | As expected
|Player loses all health | Player dies and Game over view is shown| Player dies but Game Over view doesn't appear
| Player doesn't collide with enemy| Nothing happens | As expected |

## Test 7: Enemy spawning
Date: 26/06/2023
```python
if random.random() < 0.01:
            self.enemy = arcade.Sprite(
                ':resources:images/space_shooter/meteorGrey_big4.png'
            )
            self.enemy.center_x = 500
            self.enemy.center_y = 300
            self.enemy_list.append(self.enemy)
        for self.enemy in self.enemy_list:
            self.enemy.center_x -= 2
```

| Test Data                         | Expected                                     | Observed                                      |
| --------------------------------- | -------------------------------------------- | --------------------------------------------- |
| Player collides with enemy        | Player restarts on game with one less health | As expected                                   |
| Player loses all health           | Player dies and Game over view is shown      | Player dies but Game Over view doesn't appear |
| Player doesn't collide with enemy | Nothing happens                              | As expected                                   |



## Test 8: Boss following
Date: 29/06/2023
```python
self.boss_diff_y = self.player.center_y - self.boss_center_y
        self.boss_diff_x = self.player.center_x - self.boss_center_x
        angle = atan2(self.boss_diff_y, self.boss_diff_x)
        self.boss_angle = degrees(angle)
        self.boss_change_x = 5 * cos(angle)
        self.boss_change_y = 5 * sin(angle)
```
| Test Data | Expected | Observed |
| --------- | -------- | -------- |
|               |              |             |           
|               |              |             |           |
