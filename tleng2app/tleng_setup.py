'''
First to time to click here.

Should recreate it in PyQt, which will always be pre-installed.
There is windows, linux and os x support.


setups the main files to the programfiles folder, create the neccesery trees and then creates a shortcut to the desktop. 

ProgramFiles will have (Assistant for inputing assets to your game (Import Wizard))

Tleng2 framework (currently downloaded version)
Tleng Portal (also a shorcut for desktop)
    Tleng2 Utilities (the software GUI part of the engine)
Tleng2 Example project

Portal will open a project, and use it's utilities so the user can manipulate whatever he wants
    Level Creator
    Scene Creator (special animations)
    Sprite + Animation Creator (Pixel Art) 

New projects will always give the option for a template, to kickstart the project as fast as possible

TODO: Change from pygame to PyQt
TODO: change to bash script (for linux?)

'''

import os, sys, pygame
pygame.init()

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60

def setup_main_dir_windows(parent_dir:str='C:\Program Files',directory:str= "TLeng"):
    os.chdir(parent_dir)
    path = os.path.join(parent_dir, directory) 
    os.mkdir(path) 
    print(f"Directory {directory} created") 

def setup_main_dir_linux():
    pass

def setup_main_dir_macintosh():
    '''
    I do not own a macintosh machine so it would nice if someone added the necesairy code for this to work
    '''
    pass

def main():
    run = True
    while run:
        # regulating which events are allowed (it doesn't work for some reason)
        # pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        pygame.display.update()
        CLOCK.tick(FPS)
            


if __name__ == "__main__":
    main()