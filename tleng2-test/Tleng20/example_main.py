import pygame, os, sys
from assets.scripts.Tleng2 import *

# class Particles():
WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

CLOCK = pygame.time.Clock()
FPS = 144

#maximum velocity for stickman
VEL = 200

box = Area(WIN,0,0,20,20)

#creating our stickman character
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
    stickman.display_current_anim(FPS,current_fps)
    stickman.outline_Area(4,RED)
    # TODO: PERFORMANCE SUCKER, IT SIPS PERFORMANCE LIKE CRAZY _________________________________
    # stickman.debug(WIN,['ImageX',stickman.imageX ,'ImageY',stickman.imageY, '\n',
    #                      'RectX', stickman.rect.x, 'RectY', stickman.rect.y, '\n',
    #                      f'FPS:{current_fps}'])
    pygame.display.update()

def fpsChecker(fps,lows):
    # it checks if the fps are lower than the target fps.
    if fps < FPS:
        print(f'lower {FPS-fps} from {FPS} fps! {lows} lows in total')
        return 1   
    else:
        # print(f'Higher {fps-FPS} from {FPS} fps!')
        return 0

def stickman_handle_movement(keys_pressed, stickman, dt, current_fps):
    # Using vecroting to have smooth movement
    stickman.directions.x = 0
    stickman.directions.y = 0

    if keys_pressed[pygame.K_d] and stickman.rect.x + VEL*dt + stickman.coreWidth < WIDTH: # right
        stickman.currentAnim = 'running_right'
        stickman.directions.x = 1
    
    if keys_pressed[pygame.K_a] and stickman.rect.x > 0: # right
        stickman.currentAnim = 'running_left'
        stickman.directions.x = -1
    
    if keys_pressed[pygame.K_w] and stickman.rect.y - VEL*dt > 0: # up
        stickman.directions.y = -1 

    if keys_pressed[pygame.K_s] and stickman.rect.y + VEL*dt + stickman.coreHeight < HEIGHT: # up
        stickman.directions.y = 1      

    # normalizing the vector
    if stickman.directions.x != 0 and stickman.directions.y != 0:
        stickman.directions = stickman.directions.normalize()

    stickman.imageX += stickman.directions.x * VEL * dt
    stickman.imageY += stickman.directions.y * VEL * dt


def debug_dump(lows, current_fps,stickman, dt):
    print( f"fps low: {lows}", f'fps {current_fps}, DeltaTime {dt}')
    # print(type(stickman.rect.x), type(stickman.imageX)) 

def main():
    lows = 1
    run = True
    while run:
        # getting Dt, and regulating FPS
        dt = CLOCK.tick(FPS)*0.001
        current_fps = CLOCK.get_fps()

        # regulating which events are allowed (it doesn't work for some reason)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        
        keys_pressed = pygame.key.get_pressed()
        stickman_handle_movement(keys_pressed,stickman,dt, current_fps)
        draw_window(current_fps)

        # Debugging the game performance and the game vars
        lows += fpsChecker(FPS,lows)
        debug_dump(lows,current_fps,stickman, dt)

if __name__ == "__main__":
    main()