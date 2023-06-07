# Code review 16/05


Try to put all the properties your class will ever need in the __init__
This will help with intellesence

If you put your spritelists into the scene, you'll avoid needing to call draw and update
on them individually


```python
        arcade.draw_text(str(self.health_list), 15, HEIGHT - 50, arcade.color.BLACK, font_size = 50)
```

vs

```python 
    arcade.draw_text(
        str(self.health_list), 
        15, 
        HEIGHT - 50, 
        arcade.color.BLACK, 
        font_size = 50
    )
```


Your update function is too long. Is there some duplicated code here?

Make sure to lump class definitions together and functions together. Currently load_texture_pair
is sandwhiched between two classes

Good work structuring the views well. 


# code review 7/6
- Add these points onto a KANBAN and chip away at them when you have time. 
- Use # for comments, ''' for docstrings
- keep formatting multi-line function calls as you have been. Each argument on a new line- and then the trailing bracket on its own line
```python
        self.tile_map = arcade.load_tilemap(
            './squaree.tmx', 
            layer_options=layer_options
        )
```

 - Your GUI looks like it might get advanced enough to warrant its own Scene()
 - Do you intend on having many more sounds? I feel like they sould be wrapped up in a collection. Perhaps there's a wal to loop over all the .mp3s in a folder and load them into a dict, but I haven't had anyone do this yet. 
 - bullets, enemies etc sould live in the scene
 - You are making 5 health sprites and then never adding them to a scene or spritelist
 - Same with boss health

 - line 130: same here with multi line formatting
 - line 178: you are never removing health sprites here
 - line 188: Make sure to eventually code BOSS_SPEED as a constant or a property i.e. self.boss.speed
 - Is the boss meant to take damage if the player collides with it? I would have thought the player would
 - Line 228: This won't do what you I think you think it does. Maybe self.window.show_view(game_over)
 - Line 230: Keep fixing these up
 - There are several places where the player is taking damage, consider a take_damage method to abstract this out, and remove the repetition
 - Structurally you'll have a better time if you make your views inside your window class, not your view classes
 - Tabbing in main() function is off
 - Generally you'll want to make sure you have a doc srting for each method and class
