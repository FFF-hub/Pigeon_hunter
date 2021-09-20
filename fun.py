import pygame
from pygame.locals import *
from random import randint


#variables
ENEMY_COUNTER = 0
SCORE = 0

#sprite groups
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()


#Bullet02
class Enemy_Bullet01(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, y_vel, x_vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('vis/enemy_bullet_01.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x_pos, y_pos]

        self.x_vel = x_vel
        self.y_vel = y_vel
        self.div = randint(0, 2)

    def update(self):
        self.rect.y += self.y_vel
        if self.div == 0:
            self.rect.x -= self.x_vel
        if self.div == 1:
            self.rect.x += self.x_vel

        if self.rect.bottom > 720:
            self.kill()

#Pigeons
#Default common enemy
class Pigeon01(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('vis/pigeon_01.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x_pos, y_pos]

        global ENEMY_COUNTER			#zliczanie przeciwnikow
        ENEMY_COUNTER += 1
        self.move_steps = 100
        self.move_counter = 0		#aka licznik krokow obiektu
        self.move_direction = 1
        self.hp = 1
        self.x_vel = 1				#musi byc Int !!! inaczej sie jebie
        self.y_step = 10			#liczba pikseli kroku w dol

    def update(self):
        self.rect.x += self.x_vel * self.move_direction
        self.move_counter += self.x_vel
        if abs(self.move_counter) > self.move_steps:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
        if pygame.sprite.spritecollide(self, bullet_group, True):
            self.hp -= 1
        if self.hp <= 0:
            self.kill()
            global ENEMY_COUNTER, SCORE
            ENEMY_COUNTER -= 1
            SCORE += 1

#UFO pigeon
class Pigeon02(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/pigeon_02.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]

		self.last_shot = pygame.time.get_ticks() * randint(0, 5)

		global ENEMY_COUNTER			#zliczanie przeciwnikow
		ENEMY_COUNTER += 1
		self.move_steps = 50
		self.move_counter = 0		#aka licznik krokow obiektu
		self.move_sequence = 0
		self.hp = 2
		self.x_vel = 2				#musi byc Int !!! inaczej sie jebie
		self.y_vel = 2				#oraz parzyste
		self.cooldown = 1000		#miliseconds

	def update(self):
		if self.move_sequence == 0:	#sekwencja ruchu po planie oktagonu
			self.rect.x += self.x_vel
			self.move_counter += self.x_vel
			if self.move_counter >= self.move_steps:
				self.move_sequence = 1
				self.move_counter = 0
		elif self.move_sequence == 1:
			self.rect.y += self.y_vel/2
			self.rect.x += self.x_vel/2
			self.move_counter += self.y_vel
			if self.move_counter >= self.move_steps:
				self.move_sequence = 2
				self.move_counter = 0	
		elif self.move_sequence == 2:
			self.rect.y += self.y_vel
			self.move_counter += self.y_vel
			if self.move_counter >= self.move_steps:
				self.move_sequence = 3
				self.move_counter = 0
		elif self.move_sequence == 3:
			self.rect.y += self.y_vel/2
			self.rect.x -= self.x_vel/2
			self.move_counter += self.y_vel
			if self.move_counter >= self.move_steps:
				self.move_sequence = 4
				self.move_counter = 0	
		elif self.move_sequence == 4:
			self.rect.x -= self.x_vel
			self.move_counter += self.x_vel
			if self.move_counter >= self.move_steps:
				self.move_sequence = 5
				self.move_counter = 0
		elif self.move_sequence == 5:
			self.rect.y -= self.y_vel/2
			self.rect.x -= self.x_vel/2
			self.move_counter += self.y_vel
			if self.move_counter >= self.move_steps:
				self.move_sequence = 6
				self.move_counter = 0
		elif self.move_sequence == 6:
			self.rect.y -= self.y_vel
			self.move_counter += self.y_vel
			if self.move_counter >= self.move_steps:
				self.move_sequence = 7
				self.move_counter = 0
		elif self.move_sequence == 7:
			self.rect.y -= self.y_vel/2
			self.rect.x += self.x_vel/2
			self.move_counter += self.y_vel
			if self.move_counter >= self.move_steps:
				self.move_sequence = 0
				self.move_counter = 0
		
		#record current time
		time_now = pygame.time.get_ticks()
		
		if time_now - self.last_shot > self.cooldown:
			bullet = Enemy_Bullet01(self.rect.centerx, self.rect.bottom, 4, 1)
			enemy_bullet_group.add(bullet)
			self.last_shot = time_now
		
		if pygame.sprite.spritecollide(self, bullet_group, True):
			self.hp -= 1
			
		if self.hp <= 0:
			self.kill()
			global ENEMY_COUNTER, SCORE
			ENEMY_COUNTER -= 1
			SCORE += 2
