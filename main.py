import pygame
import fun
from pygame.locals import *
from random import randint
#import fun

# CONSTANTS


# INIT VARS
SCREEN_SIZE = fun.SCREEN_SIZE


# init
#pygame.init()
#screen = pygame.display.set_mode(SCREEN_SIZE)
#pygame.display.set_caption(TITLE_)
#icon = pygame.image.load('vis/icon.png').convert()
#pygame.display.set_icon(icon)

# game control variables
GAME_RUNNING = True
change = True
CURRENT_LEVEL = 0
NEXT_LEVEL = False

# game clock
game_clock = pygame.time.Clock()
tick_counter_60 = 0

# background
background = pygame.image.load('vis/stars_1.png').convert()

# classes
# space ship


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
def create_level(enemies, arrangement):
	vector_dim = len(enemies)
	for current_position in range(vector_dim):
		create_enemies(enemies[current_position],
					   arrangement[current_position][0],
					   arrangement[current_position][1],
					   arrangement[current_position][2],
					   arrangement[current_position][3],
					   arrangement[current_position][4],
					   arrangement[current_position][5])
		
def level_complete_screen(enemies_killed, score, hp):
	fucking_somethink = 1

# Levels and player init
player = fun.Players[0]
fun.player_group.add(player)


#create enemies
level_00_enemies = [fun.Pigeon01]
level_00_geo = [[4, 6, 120, 80, 300, 100]]

level_01_enemies = [fun.Pigeon01, fun.Pigeon01]
level_01_geo = [[5, 5, 60, 40, 200, 100],
				[5, 5, 60, 40, 700, 100]]
				
level_02_enemies = [fun.Pigeon01, fun.Pigeon01,
					fun.Pigeon02]
level_02_geo = [[5, 5, 60, 40, 270, 100],
				[5, 5, 60, 40, 690, 100],
				[1, 1, 0, 0, 550, 200]]
				
level_03_enemies = [fun.Pigeon01, fun.Pigeon02,
					fun.Pigeon03]
level_03_geo = [[2, 16, 40, 40, 300, 100],
				[1, 2, 240, 120, 475, 100],
				[1, 2, 300, 120, 430, 50]]
				
level_04_enemies = [fun.Pigeon02, fun.Pigeon03]
level_04_geo = [[1, 3, 240, 120, 335, 150],
				[1, 7, 100, 120, 240, 50]]
				
level_05_enemies = [fun.Pigeon04]
level_05_geo = [[1, 5, 50, 50, 300, 150]]

level_06_enemies = [fun.Pigeon01, fun.Pigeon02,
					fun.Pigeon03, fun.Pigeon04]
level_06_geo = [[2, 16, 40, 40, 300, 100],
				[1, 3, 240, 120, 335, 150],
				[1, 2, 300, 120, 430, 50],
				[1, 3, 50, 50, 300, 150]]
				
level_07_enemies = [fun.Boss01, fun.Pigeon04]
level_07_geo = [[1, 1, 0, 0, 200, 150],
				[2, 1, 40, 40, 300, 100]]

level_map = [[level_00_enemies, level_00_geo],
			 [level_01_enemies, level_01_geo],
			 [level_02_enemies, level_02_geo],
			 [level_03_enemies, level_03_geo],
			 [level_04_enemies, level_04_geo],
			 [level_05_enemies, level_05_geo],
			 [level_06_enemies, level_06_geo],
			 [level_07_enemies, level_07_geo]]
			 
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
	player_data = player.extract_data()
	fun.player_group.update()
	
	# UI update
	fun.ui.check_player(player_data)
	fun.ui_group.update()
	fun.hp_group.update()

    # Bullet01s update
	fun.bullet_group.update()
	fun.rocket_group.update()
	fun.laser_group.update()

    # Enemies update
	fun.enemies_group.update()
	
	# Enemy bullet groups update
	fun.enemy_bullet_group.update()
    
    # level end condition
	if fun.ENEMY_COUNTER <= 0:
		NEXT_LEVEL = True
		print("CONGRATULATIONS: you have completed first encounter!")
		print("fun.SCORE: ", fun.SCORE)
		fun.bullet_group.empty()
		fun.rocket_group.empty()
		fun.enemies_group.empty()
		fun.laser_group.empty()
		fun.enemy_bullet_group.empty()
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
		print("pozostalo: ", fun.ENEMY_COUNTER, " SCORE: ", fun.SCORE)
		tick_counter_60 = 0
        
    # -----------------

# update
    #background
	fun.screen.blit(background, (0, 0))

    # player & bullets
	fun.player_group.draw(fun.screen)
	fun.bullet_group.draw(fun.screen)
	fun.rocket_group.draw(fun.screen)
	fun.laser_group.draw(fun.screen)
    # enemies
	fun.enemies_group.draw(fun.screen)
	fun.enemy_bullet_group.draw(fun.screen)
	# UI
	fun.ui_group.draw(fun.screen)
	fun.hp_group.draw(fun.screen)
	fun.screen.blit(fun.TEXT_SCORE, fun.TEXT_SCORE_XY)
	fun.screen.blit(fun.TEXT_COOLDOWNS, fun.TEXT_COOLDOWNS_XY)
	fun.screen.blit(fun.TEXT_COOLDOWNS_VAL, fun.TEXT_COOLDOWNS_VAL_XY)
    # draw
	pygame.display.update()


# exit
pygame.quit()
pygame.mixer.quit()
