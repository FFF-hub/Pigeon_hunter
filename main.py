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

# background
background = pygame.image.load('vis/stars_1.png')

# the ENEMY
enemy_pigeon_1 = pygame.image.load('vis/pigeon_01.png')
enemy_x_offset, enemy_y_offset = 16, 16
eenemy_1_x_vel, enemy_2_y_vel = 3, 3



# classes
class Entity:
    def __init__(self, name, hp, image, x_pos, y_pos, x_vel, y_vel,
                x_offset, y_offset, moved):
        self.name = name
        self.hp = hp
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.image = image
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.moved = moved


    def move(self, left, right, up, down):
        if left:
            self.x_pos -= self.x_vel
            self.moved = 0

        if right:
            self.x_pos += self.x_vel
            self.moved = 1

        if up:
            self.y_pos -= self.y_vel
            self.moved = 2

        if down:
            self.y_pos += self.y_vel
            self.moved = 3

        if not left and not right and not up and not down:
            self.moved = 4


"""
    def border_stop(self, left_lim, right_lim, up_lim, down_lim):
        if self.x_pos < left_lim:
            self.x_pos += self.x_vel
            self.moved = True
        elif self.x_pos > right_lim:
            self.x_pos -= self.x_vel
            self.moved = True


        if self.y_pos < up_lim:
            self.y_pos += self.y_vel
            self.moved = True
        elif self.y_pos > down_lim:
            self.y_pos -= self.y_vel
            self.moved = True
"""
# functions
def entity_update(entity_img, ent_x, ent_y):
    screen.blit(entity_img, (ent_x, ent_y))

def border_detect(Entity, left_lim, right_lim, up_lim, down_lim):
    if Entity.x_pos < left_lim:
        Entity.move(False, True, False, False)
    elif Entity.x_pos > right_lim:
        Entity.move(True, False, False, False)


    if Entity.y_pos < up_lim:
        Entity.move(False, False, False, True)
    elif Entity.y_pos > down_lim:
        Entity.move(False, False, True, False)

# object creation
# player
left_arrow = right_arrow = up_arrow = down_arrow = False

player = Entity('player', 3,
                  pygame.image.load('vis/player_01.png'),
                  540, 500,
                  5, 5,
                  16, 16,
                  0)

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
    player.move(left_arrow, right_arrow, up_arrow, down_arrow)

    # player border stops
    border_detect(player, 80, 1200, 80, 640)
    # -------------------

    # change checks
    if player.moved < 4:
        change = True
    # ---------------

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
    print(change, player.moved)
    if change:
        entity_update(background, 0, 0)

        entity_update(player.image,
                      player.x_pos - player.x_offset,
                      player.y_pos - player.y_offset)
        pygame.display.flip()
        change = False


# exit
pygame.quit()
