## Test 1 :
# Collecting coins

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
| Player not touching/colliding with a coin  | Nothing happens in terms of score| |
| Player touching/colliding with a coin | Score to increase by 1|  |
| Player touching/colliding with multiple coins at a time  |Score increases with the amount of coins the player collided with|  |

## Test 2 :
# Ladder logic
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
| Player standing still on ladder| Player is able to standing still facing the direction they were jumping to | |