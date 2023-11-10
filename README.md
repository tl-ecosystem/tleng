# TLengPy2

Tleng engine, is a game engine written in python and based on the pygame library. For the Engine to work, you need to have installed pygame!

The reason I started this project is to see what it takes to create a 2d game engine, and for me to get an even better introduction to computer 2d graphics.

The code is here to either inspire someone else to start a similar project, or to give some insight on a few things.

## Games that use this engine/framework:

- [RainCoin](https://github.com/TheooKing/RainCoin) (Framework ver: 2.0-dev (modded))
- [CoulomHelper](https://github.com/TheooKing/CoulombHelper)

## Requirements
- python 3.11+
- Pygame 2.3+ or Pygame Community Edition 2.2+
- matplotlib 3.6+ (for debugging with graphs)
- numpy 1.24+ 


## The planned full releases are:

- 2.0 Documentation and publication of git page 

- 2.2 re-structure of the engine, sound and camera-scene handlers, additional software full release ( <- we are here)

- 2.3 Available package at PyPi.org + collisions update, particles, (AI, missions async update) 

- 2.4 Physics implementation module

- 2.5 Full Raycasting support

- 2.6 Sprite stacking & voxel engine support

- 2.7 Multiplayer support

On every single update there will always be an example, in the example folder.

## Additional Bundled Software for TLengPy2

This software will have a GUI for the user

- Level Creator
- Assistant for inputing assets to your game (Import Wizard)
- Scene Creator
- Sprite + Animation Creator (Pixel Art)

## The meaning behind the symbolising of the updates are 2.x.y-z:

2 = the engine is 2d (and because it's better than the previous try)

x = The general full release version 

y = The bug fix version for the general release

z = is either Beta/Alpha/dev of the general release or the bug fix version


## Short code documantation:

### Classes:

 - Area

You can create an Area, a box, that could act a hitbox or what you want it to look like then call it to be drawn with `draw_Area()`, or for the outline to be drawn with `outline_Area()`.

 - Label

You can create text with `set_Label()` and then call it to be drawn with `draw_Label()`

 - Entity

You can show Animations with `display_current_anim()` which you can control how fast or slow tha animation goes, the animation is also always frame independant, meaning that whatever you put the framerate at, it will always print at the same speed. You also have the power to transform images with `flip_img()` and `transform_img()`. 

 - Object

Not implemented yet

 - Projectile

Not implemented yet

 - Particles

Not implemented yet
 
 ### The contributor of the main branch is Theolaos (@Thooking007).
