import pygame
from random import randint

# CONSTANTS
TITLE_ = "Pigeon Hunter I"

# INIT VARS
SCREEN_SIZE = (1280, 720)

game_running = True

# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(TITLE_)

    # game clock
game_clock = pygame.time.Clock()

# player
player_crosshair = pygame.image.load('vis/crosshair.png')
player_crosshair_offset_x = -32;
player_crosshair_offset_y = -32;

# background
background = pygame.image.load('vis/minsk.png')

# the ENEMY
enemy_pigeon_1 = pygame.image.load('vis/pigeon_01.png')


# game loop
while game_running:

    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                game_running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()



    # update

    # draw
    screen.blit(background, (0, 0))
    screen.blit(player_crosshair, (mouse_x + player_crosshair_offset_x,
                                   mouse_y + player_crosshair_offset_y))
    pygame.display.flip()

# exit
pygame.quit()
