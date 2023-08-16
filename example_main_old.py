import pygame, os, sys
from assets.scripts.engine.Tleng2 import *
from time import time
import numpy as np
import matplotlib.pyplot as plt

# TODO: for some reason the button has a smaller hitbox than the image
# class Particles():
WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

# print(type(WIN))
pygame.display.set_caption("Sample Version 2.2-exp")

CLOCK = pygame.time.Clock()
FPS = 2000

#maximum velocity for stickman
VEL = 200

#for debugging

# debugging = Debug(WIN, 0, 0, 10, 10, '')


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


def print1():
    print("Hello World -------------------------------------")

button = Button(WIN, 50, 600, 'action', 400, 50, callback=print1)


def draw_window(current_fps):
    #reseting the backgoround to it's original color
    WIN.fill(BLACK)  
    box.draw_Area()
    box.outline_Area(-2,RED)
    stickman.draw_current_anim(FPS,current_fps)
    stickman.outline_Area(4,RED)
    # print(stickman.rect.bottomright)
    # debugging.update(stickman.rect.width + stickman.rect.x, stickman.rect.height + stickman.rect.y,
    #                  text=['Image\nX',stickman.imageX ,'\nImageY',stickman.imageY, '\n',
    #                       'RectX', stickman.rect.x, 'RectY', stickman.rect.y, '\n',
    #                       f'FPS:{current_fps}'])
    button.simple_draw()
    pygame.display.update()




def fpsChecker(fps,lows):
    # it checks if the fps are lower than the target fps.
    if fps < FPS:
        print(f'lower {FPS-fps} from {FPS} fps! {lows} lows in total')
        return 1   
    else:
        # print(f'Higher {fps-FPS} from {FPS} fps!')
        return 0

def stickman_handle_movement(keys_pressed, stickman, dt, current_fps): # TODO: there is room for optimization
    # Using vectoring to have smooth movement
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
    # stickman.rect.centerx += stickman.directions.x * VEL * dt
    # stickman.rect.centery += stickman.directions.y * VEL * dt


def average_of(total:list, max:int|None =None) -> float:
    sum1 = 0
    if max != None:
        for i in range(max):
            sum1 += total[i]
    
    else:
        for i in total:
            sum1 += i

    return sum1/len(total)

def showgraph(total_fps):
    x = np.arange(len(total_fps))
    y = []
    for i in total_fps:
        y.append(i)

    y = np.array(y)
    plt.scatter(x, y)
    plt.plot(x, y)
    plt.show()

def time_based_dt(dt1, dt2) -> float:
    return dt2 - dt1

def main():
    lows = 1
    run = True
    previous_fps = 0
    total_fps = []
    fps = 1
    frame = 0
    start_of_frame = time()
    end_of_frame = None
    start_fps = time()
    fps_dt = 1

    dt_list=[]
    while run:
        # frame += 1
        # # getting Dt, and regulating FPS
        # if time() - start_fps >= 1:
        #     fps = frame
        #     frame = 0
        #     start_fps = time()
        
        # if time() - start_fps >= 1:
        #     fps = 1/dt
        

        # dt = 1/fps
        # dt_list += [dt]
        # fps_dt = 1/average_of(dt_list) 
        
        # # print(len(dt_list), dt_list)
        # if len(dt_list) > 10:
        #     # print(average_of(dt_list, 10), dt_list)
        #     dt_list.remove(dt_list[0])

        # current_fps = fps
        
        # print(frame, fps_dt, dt)
        dt = CLOCK.tick(FPS)*0.001
        current_fps = CLOCK.get_fps()

        # regulating which events are allowed (it doesn't work for some reason)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print(f'Total average fps: {average_of(total_fps)} ')
                showgraph(total_fps)
                
                pygame.quit()
                sys.exit()
            button.handle_event(event)
        
        keys_pressed = pygame.key.get_pressed()
        stickman_handle_movement(keys_pressed,stickman,dt, current_fps)
        draw_window(current_fps)

        # Debugging the game performance and the game vars
        # lows += fpsChecker(FPS,lows)
        previous_fps = current_fps
        total_fps += [previous_fps]




if __name__ == "__main__":
    main()
