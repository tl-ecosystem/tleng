# TLeng2

(I am new to github so the helping (pulling requests, branches and such) stuff is something i don't quite get yet)

Tleng engine, is an engine written in python and based on the pygame library. For the Engine to work, you need to have installed pygame!

The reason I started this project is to see what it takes to create a 2d game engine, and for me to get an even better introduction to computer 2d graphics.

The code displayed here, is open to be used by anyone. If someone wants to add something, could either tell me or do it himself, by pulling a request.

The code is here to either inspire someone else to start a similar project, or to give some insight on a few things.

## The planned full releases are:

- 2.0 Documentation and publication of git page 

- 2.1 Hitbox and Coordination, additional software (experimental) (simplify code, update/implement TODOs, examples) ( <- we are here)

- 2.2 sound and camera-scene handlers, additional software full release

- 2.3 Available package at PyPi.org + collisions update, particles, (AI, missions async update) 

- 2.4 Physics implementation module

- 2.5 Multiplayer support

- 2.6 Full Raycasting support

On every single update there will always be an example, in the example folder.

## There will be additional Software that will work like a bundle for TLeng2

This software will have a GUI for the user

- Level Creator
- Assistant for inputing assets to your game (Import Wizard)
- Scene Creator
- Sprite + Animation Creator (Pixel Art)

### The meaning behind the symbolising of the updates are 2.x.y-z:

2 = the engine is 2d (and because it's better than the previous try)

x = The general full release version 

y = The bug fix version for the general release

z = is either Beta/Alpha of the general release or the bug fix version





## Short code documantation:

### Classes:

 -Area

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
