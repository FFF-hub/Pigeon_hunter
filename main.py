import pygame
from pygame.locals import *
from random import randint
#import fun

# CONSTANTS
TITLE_ = "Space Pigeons"

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
# space ship
class Player(pygame.sprite.Sprite):
    def __init__(self, name, hp, x_pos, y_pos, vel, cooldown):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('vis/player_01.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x_pos, y_pos]

        self.last_shot = pygame.time.get_ticks()

        self.hp = hp
        self.name = name
        self.vel = vel
        self.cooldown = cooldown #milliseconds

        #player movement
    def update(self):
        #key presses
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vel
        if key[pygame.K_RIGHT] and self.rect.right < SCREEN_SIZE[0]:
            self.rect.x += self.vel
        if key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.vel
        if key[pygame.K_DOWN] and self.rect.bottom < SCREEN_SIZE[1] :
            self.rect.y += self.vel

        #record current time
        time_now = pygame.time.get_ticks()

        #abilities
            # Q - default GUN
        if key[pygame.K_q] and time_now - self.last_shot > self.cooldown:
            bullet = Bullet01(self.rect.centerx, self.rect.top, 8, 1)
            bullet_group.add(bullet)
            self.last_shot = time_now

        if self.hp <= 0:
            self.kill()

#Bullet01
class Bullet01(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, y_vel, x_vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('vis/bullet_01.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x_pos, y_pos]

        self.x_vel = x_vel
        self.y_vel = y_vel
        self.div = randint(0, 12)

    def update(self):
        self.rect.y -= self.y_vel
        if self.div == 0:
            self.rect.x -= self.x_vel
        if self.div == 1:
            self.rect.x += self.x_vel

        if self.rect.bottom < 0:
            self.kill()


#Pigeons
class Pigeon01(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('vis/pigeon_01.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x_pos, y_pos]

        self.move_counter = 0
        self.move_direction = 1
        self.hp = 1
        self.x_vel = 1
        self.y_step = 10

    def update(self):
        self.rect.x += self.x_vel * self.move_direction
        self.move_counter += self.x_vel
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
        if pygame.sprite.spritecollide(self, bullet_group, True):
            self.hp -= 1
        if self.hp <= 0:
            self.kill()

#sprite groups
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

#enemy creator
def create_enemies(enemy_type, rows, cols, x_dis, y_dis, x_buf, y_buf):
    for row in range (rows):
        for item in range(cols):
            enemy = enemy_type(x_buf + item * x_dis, y_buf + row * y_dis)
            enemies_group.add(enemy)

#create player
player = Player('player', 3, int(SCREEN_SIZE[0] / 2), SCREEN_SIZE[1] - 200,
                5, 750)
player_group.add(player)

#create enemies

create_enemies(Pigeon01, 5, 5, 60, 40, 100, 100)

# game loop
while game_running:

    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                game_running = False

    # player update
    player.update()

    # Bullet01s update
    bullet_group.update()

    # Enemies update
    enemies_group.update()

# game clock idk

    # game clock stuff
    game_clock.tick(58)
    if tick_counter_60 < 60:
        tick_counter_60 += 1
    else:
        print(game_clock.get_fps())
        tick_counter_60 = 0
    # -----------------

# update
    #background
    screen.blit(background, (0, 0))

    # player & bullets
    player_group.draw(screen)
    bullet_group.draw(screen)
    # enemies
    enemies_group.draw(screen)
    # draw
    pygame.display.update()


# exit
pygame.quit()
