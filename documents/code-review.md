# Code review 16/05

don't use `from math import *`. Just import what you need

Try to put all the properties your class will ever need in the __init__
This will help with intellesence

If you put your spritelists into the sceen, you'll avoid needing to call draw and update
on them individually

some lines getting too long. Try breaking them up. 

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

You need lots of comments \ docstrings. Every function and every class needs a docstring

Your update function is too long. Is there some duplicated code here?

Make sure to lump class definitions together and functions together. Currently load_texture_pair
is sandwhiched between two classes

Good work structuring the views well. 

