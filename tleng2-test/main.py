import pygame, os
pygame.init()

from assets.scripts.Tleng2 import *

# class Particles():
WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

CLOCK = pygame.time.Clock()
FPS = 1000

#maximum velocity for stickman
VEL = 10

box = Area(WIN,0,0,20,20)

stickman = Entity(WIN,50,50,60,60,"player",RED,{
    "running_left":[os.path.join('assets','art','pictures','animations',"walking",'walkingman1.png'),
                 os.path.join('assets','art','pictures','animations',"walking",'walkingman2.png'),
                 os.path.join('assets','art','pictures','animations',"walking",'walkingman3.png'),
                 os.path.join('assets','art','pictures','animations',"walking",'walkingman4.png')],

    "running_right":[os.path.join('assets','art','pictures','animations',"walking",'walkingman1.png'),
                 os.path.join('assets','art','pictures','animations',"walking",'walkingman2.png'),
                 os.path.join('assets','art','pictures','animations',"walking",'walkingman3.png'),
                 os.path.join('assets','art','pictures','animations',"walking",'walkingman4.png')],

    "jumping":[os.path.join('assets','art','pictures','animations','jumping','jumping1.png'),
                 os.path.join('assets','art','pictures','animations','jumping','jumping2.png'),
                 os.path.join('assets','art','pictures','animations','jumping','jumping3.png'),
                 os.path.join('assets','art','pictures','animations','jumping','jumping4.png')]},

os.path.join('assets','art','pictures','standingman.png'))

stickman.flip_img(['running_right'], (True,False))

def draw_window(current_fps):
    WIN.fill(BLACK)
    box.draw_Area()
    box.outline_Area(-2,RED)
    stickman.display_current_anim(fps=current_fps)
    stickman.outline_Area(10,RED)
    pygame.display.update()

def fpsChecker(fps,lows):
    if fps < FPS:
        print(f'lower {FPS-fps} from {FPS} fps! {lows} lows in total')
        return 1   
    else:
        # print(f'Higher {fps-FPS} from {FPS} fps!')
        return 0

def stickman_handle_movement(keys_pressed, stickman):
    if keys_pressed[pygame.K_a] and stickman.rect.x - VEL > 0: # left
        stickman.currentAnim = 'running_left'
        stickman.rect.x -= VEL
        stickman.coreX -= VEL

    if keys_pressed[pygame.K_d] and stickman.rect.x + VEL + stickman.coreWidth < WIDTH: # right
        stickman.currentAnim = 'running_right'
        stickman.rect.x += VEL
    if keys_pressed[pygame.K_w] and stickman.rect.y - VEL > 0: # up
        stickman.rect.y -= VEL
    if keys_pressed[pygame.K_s] and stickman.rect.y + VEL + stickman.coreHeight < HEIGHT: # down
        stickman.rect.y += VEL

def debug_dump(lows, current_fps):
    print(stickman.coreX,stickman.coreY, f"fps low: {lows}", f'fps {current_fps}')

def main():
    lows = 1
    run = True
    while run:
        CLOCK.tick(FPS)
        current_fps = CLOCK.get_fps()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        keys_pressed = pygame.key.get_pressed()
        stickman_handle_movement(keys_pressed,stickman)
        lows += fpsChecker(FPS,lows)
        draw_window(current_fps)
        debug_dump(lows,current_fps)

        


if __name__ == "__main__":
    main()