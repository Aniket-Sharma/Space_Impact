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
screen_width = math.floor(infoObject.current_w * 0.6)
screen_height = math.floor(infoObject.current_h * 0.7)
win = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

pygame.display.set_caption("Space impact: Level 1")

# Define the Shuttle properties
live = 3
x = 10
y = screen_height/2
vel = screen_height/100
shuttle_width = math.floor(screen_width * 0.05)
Shuttle_height = math.floor(screen_height * 0.05)

# Define bullets
pygame.time.set_timer(USEREVENT+1, 1000)
bullets = []
step = 10

# Define obstracles
pygame.time.set_timer(USEREVENT+2, 10000)
first_enemy = []

# the redraw game window function
def redrawGameWindow():
    win.fill((BLACK))
    pygame.draw.rect(win, BLUE, (x, y, shuttle_width, Shuttle_height))
    for bullet in bullets:
        if bullet[0] >= screen_width:
            bullets.remove(bullet)
        else:
            bullet[0]+=step
        pygame.draw.circle(win, RED, bullet, 4, 0)
    for enemy in first_enemy:
        if enemy[0] <= 0:
            first_enemy.remove(enemy)
        else:
            enemy[0] -= First.step
        pygame.draw.circle(win, RED, (enemy[0], enemy[1]), 4, 0)
        pygame.draw.rect(win, NAVY, (enemy[0], enemy[1], First.width, First.height))
    pygame.display.update()

# first obstracles : straight moving things
class First:
    power = 2
    step = 2
    width = 10
    height = 5
    def create_new_first_enemy():
        first_x = screen_width
        first_y = random.randint(10,screen_height-10)
        new_obs = [first_x, first_y, First.power]
        first_enemy.append(new_obs)
## the main loop
run = True
while run :
    pygame.time.delay(100)

    #define the basic quit function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == USEREVENT+1:
            temp_x = math.floor(x+shuttle_width)
            temp_y = math.floor(y+(Shuttle_height/2))
            pos = [temp_x, temp_y]
            bullets.append(pos)

        if event.type == USEREVENT+2:
            First.create_new_first_enemy()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel

    if keys[pygame.K_RIGHT] and x < screen_width - shuttle_width - vel :
        x += vel

    if keys[pygame.K_UP] and y > vel:
        y -= vel

    if keys[pygame.K_DOWN] and y < screen_height - Shuttle_height - vel :
        y += vel

    redrawGameWindow()

pygame.quit()
