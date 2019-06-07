import pygame
import random
import math
from pygame.locals import *
pygame.init()

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
NAVY =   (0,   0,   128)

#basic colors
black = (0,0,255)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
bright_green = (0,128,0)
bright_red = (128,0,0)

clock = pygame.time.Clock()

#define the screen properties
infoObject = pygame.display.Info()
screen_width = math.floor(infoObject.current_w * 1.0)
screen_height = math.floor(infoObject.current_h * 0.9)
win = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

pygame.display.set_caption("F1 Racing")

# Define the Shuttle properties
lanes = 7
lane_size = math.floor(screen_height/lanes)

vel = screen_height/50

Shuttle_width = math.floor(screen_width/12)
Shuttle_height = math.floor(screen_height/(lanes+3))
margin = math.floor(lane_size - Shuttle_height)
x = 0
y = math.floor(((lanes-1)/2) * lane_size) + margin/2

#Define global variables
score = 0

# Define upcoming cars 
cars = []
step = 5

#Define the level Properties
level = 1
level_threshhold = 10
level_obs_count = 0 
step_increase = 1 
max_level = 10

#the timer for new Obstecle creation
timer = 1000 #in microseconds
pygame.time.set_timer(USEREVENT+1, timer)

#define button
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(win, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(win, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    win.blit(textSurf, textRect)

#define the freeze function
def froze():
    while True : 
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        k = pygame.key.get_pressed()
            
        if k[pygame.K_LEFT] or k[pygame.K_RIGHT] or k[pygame.K_UP] or k[pygame.K_DOWN] :
            break
        
#function after if crash occured
def crashed():
    global score
    msg = 'GAME OVER You Scored :' + str(score)
    pause = True
    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        win.fill(white)
        
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = (((screen_width/2)), ((screen_height/3)) )
        win.blit(textSurf, textRect)
        
        button("EXIT",600,250,200,100,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)
        
# a function to crete a new car
def quitgame():
    pygame.quit()
    quit()
    
def create_new_car():
    global cars
    global level, step, vel, level_threshhold, level_obs_count, step_increase, score, max_level
    cor_x = screen_width
    lane = random.randint(1, lanes)
    cor_y = math.floor(((lane-1) * lane_size) + margin/2)
    new_car = [cor_x, cor_y]
    cars.append(new_car)
    
    return

# the redraw game window function
def redrawGameWindow():
    global level, step, vel, level_threshhold, level_obs_count, step_increase, score, max_level
    win.fill((BLACK))
    
    shuttle = pygame.Rect(x, y, Shuttle_width, Shuttle_height)
    pygame.draw.rect(win, BLUE, (x, y, Shuttle_width, Shuttle_height))

    j = 0 
    for i in range(len(cars)):
        cars[i][0] = cars[i][0] - step
        if cars[i][0] <= -Shuttle_width:
            j += 1
            score += 1
            level_obs_count += 1
            if level_obs_count == level_threshhold:
                level_obs_count = 0 
                level += 1
                if level <= max_level :
                    step += step_increase
                    vel += step_increase
    del(cars[:j])  
            
    for car in cars:
        car = pygame.Rect(car[0], car[1], Shuttle_width, Shuttle_height)
        if car.colliderect(shuttle):
            pygame.time.delay(2000)
            crashed()
        pygame.draw.rect(win, RED, (car[0], car[1], Shuttle_width, Shuttle_height))

    # Drawing lines for showing lanes
    for lane in range(lanes+2):
        y_cor = (lane-1) * lane_size
        pygame.draw.line(win, WHITE, [0, y_cor], [screen_width, y_cor])

    msg = 'Score : ' + str(score) + '  Level : ' + str(level) + '  Speed :' + str(step)
    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((screen_width/2), (screen_height-10) )
    win.blit(textSurf, textRect)
    pygame.display.update()

## the main loop
    
run = True
while run :
    #define the basic quit function
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False

        if event.type == USEREVENT + 1:
            create_new_car()
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel

    if keys[pygame.K_RIGHT] and x < screen_width - Shuttle_width - vel :
        x += vel

    if keys[pygame.K_UP] and y > vel:
        y -= vel

    if keys[pygame.K_DOWN] and y < screen_height - Shuttle_height - vel :
        y += vel
                
    if keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE] :
        froze()

    redrawGameWindow()
    pygame.time.delay(50)

print(score)
pygame.quit()
