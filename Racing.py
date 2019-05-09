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

#define the screen properties
infoObject = pygame.display.Info()
screen_width = math.floor(infoObject.current_w * 1)
screen_height = math.floor(infoObject.current_h * 0.9)
win = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

pygame.display.set_caption("F1 Racing")

# Define the Shuttle properties
lanes = 7
lane_size = math.floor(screen_height/lanes)
vel = screen_height/50
shuttle_width = math.floor(screen_width/12)
Shuttle_height = math.floor(screen_height/(lanes+3))
margin = math.floor(lane_size - Shuttle_height)
x = 0
y = math.floor(((lanes-1)/2) * lane_size) + margin/2

#Define global variables
score = 0

# Define upcoming cars
cars = []
updated_cars = []
step = 5
level = 1
if level <= 10:
    timer = math.floor(10000/level)
    pygame.time.set_timer(USEREVENT+1, timer)

# a function to crete a new car
def create_new_car():
    cor_x = screen_width
    lane = random.randint(1, lanes)
    cor_y = math.floor(((lane-1) * lane_size) + margin/2)
    new_car = [cor_x, cor_y]
    return new_car

# the redraw game window function
def redrawGameWindow():
    win.fill((BLACK))
    pygame.draw.rect(win, BLUE, (x, y, shuttle_width, Shuttle_height))

    updated_cars = cars
    for car in updated_cars:
        car[0] = car[0] - step - level
        if car[0] <= -100:
            cars.remove(car)
            global score
            score += 1
        pygame.draw.rect(win, RED, (car[0], car[1], shuttle_width, Shuttle_height))

    # Drawing lines for showing lanes
    for lane in range(lanes+2):
        y_cor = (lane-1) * lane_size
        pygame.draw.line(win, WHITE, [0, y_cor], [screen_width, y_cor])

    pygame.display.update()

## the main loop
run = True
while run :
    pygame.time.delay(100)
    #define the basic quit function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == USEREVENT+1:
            pos = create_new_car()
            cars.append(pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel

    if keys[pygame.K_RIGHT] and x < screen_width - shuttle_width - vel :
        x += vel

    if keys[pygame.K_UP] and y > vel:
        y -= vel

    if keys[pygame.K_DOWN] and y < screen_height - Shuttle_height - vel :
        y += vel

    level = math.ceil(len(cars)/10)
    redrawGameWindow()

print(score)
pygame.quit()
