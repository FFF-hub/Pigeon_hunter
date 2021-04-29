import pygame
from random import randint
#import fun

# CONSTANTS
TITLE_ = "Pigeon Hunter I"

# INIT VARS
SCREEN_SIZE = (1280, 720)

game_running = True

# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(TITLE_)
icon = pygame.image.load('vis/icon.png')
pygame.display.set_icon(icon)

# game control variables
change = True

# game clock
game_clock = pygame.time.Clock()
tick_counter_60 = 0

# player
player_ship = pygame.image.load('vis/player_01.png')
player_x, player_y = 640, 600
player_x_offset, player_y_offset = 16, 16
left_arrow = right_arrow = up_arrow = down_arrow = False
x_vel, y_vel = 5, 5
mov_block_x = mov_block_y = False

# background
background = pygame.image.load('vis/stars_1.png')

# the ENEMY
enemy_pigeon_1 = pygame.image.load('vis/pigeon_01.png')

# functions
def entity_update(entity_img, ent_x, ent_y):
    screen.blit(entity_img, (ent_x, ent_y))


# game loop
while game_running:

    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                game_running = False
        # Keys pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_arrow = True
            if event.key == pygame.K_RIGHT:
                right_arrow = True
            if event.key == pygame.K_UP:
                up_arrow = True
            if event.key == pygame.K_DOWN:
                down_arrow = True
        # Keys unpressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_arrow = False
            if event.key == pygame.K_RIGHT:
                right_arrow = False
            if event.key == pygame.K_UP:
                up_arrow = False
            if event.key == pygame.K_DOWN:
                down_arrow = False
        # ------------------------

    # player movement
    if left_arrow:
        player_x -= x_vel
        change = True
    if right_arrow:
        player_x += x_vel
        change = True
    if up_arrow:
        player_y -= y_vel
        change = True
    if down_arrow:
        player_y += y_vel
        change = True

    if player_x < 80:
        player_x += x_vel
    elif player_x > 1200:
        player_x -= x_vel
    # -------------------

    # player wall bounds
    if player_y < 80:
        player_y += y_vel
    elif player_y > 640:
        player_y -= y_vel
    # -------------------

# game clock idk

    # game clock stuff
    game_clock.tick(58)
    if tick_counter_60 < 60:
        tick_counter_60 += 1
    else:
        print(game_clock.get_fps())
        tick_counter_60 = 0
    # ---------------------

# update

    # draw
    if change:
        entity_update(background, 0, 0)
        entity_update(player_ship, player_x - player_x_offset, player_y - player_y_offset)
        pygame.display.flip()
        change = False


# exit
pygame.quit()
