import pygame
import fun
from pygame.locals import *
from random import randint
#import fun

# CONSTANTS
TITLE_ = "Space Pigeons"

# INIT VARS
SCREEN_SIZE = (1200, 720)



# init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(TITLE_)
icon = pygame.image.load('vis/icon.png')
pygame.display.set_icon(icon)

# game control variables
GAME_RUNNING = True
change = True
CURRENT_LEVEL = 0
NEXT_LEVEL = False

# game clock
game_clock = pygame.time.Clock()
tick_counter_60 = 0

# background
background = pygame.image.load('vis/stars_1.png')

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

	def extract_data(self):
		return self.name, self.hp, self.vel, self.cooldown

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
			fun.bullet_group.add(bullet)
			self.last_shot = time_now

		if self.hp <= 0:
			self.kill()
			
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

#enemy creator
def create_enemies(enemy_type, rows, cols, x_dis, y_dis, x_buf, y_buf):
	# x_buf/y_buf - odpowiadaja za odstep od krawedzi ekranu (x/y)
    for row in range(rows):
        for item in range(cols):
            enemy = enemy_type(x_buf + item * x_dis, y_buf + row * y_dis)
            fun.enemies_group.add(enemy)

#level creator function
# enemies = [pigeon01, pigeon02, ..., pigeonN]
# arrangement = [[rows, cols, x_dis, y_dis, x_buf, y_buf], ..., '']
def create_level(enemies, arrangement, ):
	vector_dim = len(enemies)
	for current_position in range(vector_dim):
		create_enemies(enemies[current_position],
					   arrangement[current_position][0],
					   arrangement[current_position][1],
					   arrangement[current_position][2],
					   arrangement[current_position][3],
					   arrangement[current_position][4],
					   arrangement[current_position][5])
		

# Level zero
player = Player('player', 3, int(SCREEN_SIZE[0] / 2), SCREEN_SIZE[1] - 200,
                5, 750)
fun.player_group.add(player)

#create enemies
level_00_enemies = [fun.Pigeon03]
level_00_geo = [[2, 2, 120, 80, 350, 100]]

level_01_enemies = [fun.Pigeon01, fun.Pigeon01]
level_01_geo = [[5, 5, 60, 40, 200, 100],
				[5, 5, 60, 40, 750, 350]]

level_map = [[level_00_enemies, level_00_geo],
			 [level_01_enemies, level_01_geo]]
			 
MAX_LEVEL = len(level_map) - 1

create_level(level_00_enemies, level_00_geo)
# End of Level zero

# game loop
while GAME_RUNNING:

    # input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME_RUNNING = False

    # player update
	player.update()

    # Bullet01s update
	fun.bullet_group.update()

    # Enemies update
	fun.enemies_group.update()
	
	# Enemy bullet groups update
	fun.enemy_bullet_group.update()
    
    # level end condition
	if fun.ENEMY_COUNTER <= 0:
		NEXT_LEVEL = True
		print("CONGRATULATIONS: you have completed first encounter!")
		print("fun.SCORE: ", fun.SCORE)
		# level creation function here
		# position of player with data from previous lvl
		# new locations of enemies
		if CURRENT_LEVEL < MAX_LEVEL:
			CURRENT_LEVEL += 1
		else:
			NEXT_LEVEL = False
			GAME_RUNNING = False
			print("CONGRATULATIONS YOU HAVE SAVED THE GALAXY")
	
	if NEXT_LEVEL:
		print("COMMING UP! LEVEL: ", CURRENT_LEVEL)
		create_level(level_map[CURRENT_LEVEL][0],
					level_map[CURRENT_LEVEL][1])
		NEXT_LEVEL = False
		
# game clock idk

    # game clock stuff
	game_clock.tick(58)
	if tick_counter_60 < 60:
		tick_counter_60 += 1
	else:
		print(game_clock.get_fps())
		print("pozostalo: ", fun.ENEMY_COUNTER)
		tick_counter_60 = 0
        
    # -----------------

# update
    #background
	screen.blit(background, (0, 0))

    # player & bullets
	fun.player_group.draw(screen)
	fun.bullet_group.draw(screen)
    # enemies
	fun.enemies_group.draw(screen)
	fun.enemy_bullet_group.draw(screen)
    # draw
	pygame.display.update()


# exit
pygame.quit()
