# TLeng2

> ## :warning: WARNING 
>
> The game engine is still in the early stages, so please note that for every new push it is not guranteed that the new code will reliably work with your previous or current projects. Check the releases before attempting to get the newest from source.

 ![Static Badge](https://img.shields.io/badge/pip_install-tleng-blue?style=flat) ![Static Badge](https://img.shields.io/badge/licence-MIT-blue?style=flat) ![Static Badge](https://img.shields.io/badge/python-3.11_3.12-blue?style=flat&logo=python)



TLeng2 (pronounced: tlenk-two) is a game engine that supports python (with the pygame-ce, pymunmk and NumPy modules) and C++. 

The reason I started this project is to see what it takes to create a 2d game engine, and for me to get an even better introduction to computer 2d graphics.

The code is here to either inspire someone else to start a similar project, or to give some insight on a few things.

On every single general release update there always will be an example game, in the `examples` folder.

The C++ version of the engine is a work in progress, but it will be available soon! 

After the C++ section will be finished, the engine will change names from TLeng2 to TLeng3. TLeng2 aims only for support with python, TLeng3 aims to support python and C++ together.

## Setting Up the Engine

It is recommended that everytime you create a game in `Tleng` you create a `Virtual Enviroment`. That is to resolve any conflicts that might arise from namespaces and more (`Tleng` uses `Pygame-CE` which conflicts with `Pygame`).

Here is how to create a `virtual enviroment`:
```bash
$ python -m venv name_of_your_virtual_enviroment
```

Then you want to activate the `virtual enviroment`:
```bash
$ source venv/bin/activate
```

Now install the `TLeng` game engine with `pip`:
```bash
$ pip install tleng
```

Create a directory that is going to host your game files:
```bash
$ mkdir my_game_name
$ cd my_game_name
```

After that you can create a `main.py` file:

```bash
$ touch main.py
$ your_preferred_editor main.py
```

Import `tleng2` and start developing games!

## 📖 Documentation

Check the github [wiki](https://github.com/tl-ecosystem/tleng/wiki)!

## 🎮 Games that use this engine/framework:

- [RainCoin](https://github.com/theolaos/RainCoin) (Framework ver: 2.0-dev)
- [ScalarTux](https://github.com/theolaos/ScalarTux) (In development, Framework ver: v2.2.0.dev4)
- [PixelWheel](https://github.com/Omilos-Plhroforikis-17o-GEL-13o-GYM/pixel-wheel) (In development, Framework ver: v2.2.0.dev12)

## 🛠️ Requirements
- Python:
  - python 3.11+
  - Pygame Community Edition 2.2+
  - PyMunk 6.5+
  - NumPy 1.20+
  - ModernGL (not needed yet)
- C++ (WIP):
  - SDL 3
  - GLAD
  - OpenGL
  - CMake

## 💾 Additional Bundled Software for TLengPy2 (in development)

This software will have a GUI for the user

- [SpriteStacking Viewer](https://github.com/tl-ecosystem/tl-ssv)
- Tilemap Editor
- Level Creator
- Assistant for inputing assets to your game (Import Wizard)
- Scene/UI Creator
- Animation Creator

## ❓ The meaning behind the symbolising of the updates are 2.x.y.z:

2 = the engine is 2d (and because it's better than the previous try)

x = The general full release version 

y = The bug fix version for the general release

z = is either Beta/Alpha/dev/exp of the general release or the bug fix version (exp : experimental)
 
### The contributor of the main branch is Theolaos (@theolaos).
