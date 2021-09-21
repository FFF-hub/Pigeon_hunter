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
#shrapnel  
class Enemy_Shrapnel01(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos, y_vel, x_vel):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/enemy_shrapnel_01.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]

		self.x_vel = x_vel
		self.y_vel = y_vel
		self.move_counter = 0
		self.move_steps = 500

	def update(self):
		self.rect.y += self.y_vel
		self.rect.x += self.x_vel
		self.move_counter += self.y_vel + self.x_vel
        
		if self.move_counter >= self.move_steps:
			self.kill()

		if self.rect.bottom > 720 or self.rect.top < 0 or self.rect.right > 1200 or self.rect.left < 0:
			self.kill()


#Egg 1
class Enemy_Egg01(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos, y_vel, x_vel):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/enemy_egg_01.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]

		self.move_steps = randint(200, 800)
		self.move_counter = 0
		self.y_vel = y_vel
		self.div = randint(0, 2)

	def explode(self):
		bullet0 = Enemy_Shrapnel01(self.rect.centerx, self.rect.bottom,  0, 3)
		bullet1 = Enemy_Shrapnel01(self.rect.centerx, self.rect.bottom,  2, 2)
		bullet2 = Enemy_Shrapnel01(self.rect.centerx, self.rect.bottom,  3, 0)
		bullet3 = Enemy_Shrapnel01(self.rect.centerx, self.rect.bottom,  -2, 2)
		bullet4 = Enemy_Shrapnel01(self.rect.centerx, self.rect.bottom,  0, -3)
		bullet5 = Enemy_Shrapnel01(self.rect.centerx, self.rect.bottom,  -2, -2)
		bullet6 = Enemy_Shrapnel01(self.rect.centerx, self.rect.bottom,  -3, 0)
		bullet7 = Enemy_Shrapnel01(self.rect.centerx, self.rect.bottom,  2, -2)
		
		enemy_bullet_group.add(bullet0)
		enemy_bullet_group.add(bullet1)
		enemy_bullet_group.add(bullet2)
		enemy_bullet_group.add(bullet3)
		enemy_bullet_group.add(bullet4)
		enemy_bullet_group.add(bullet5)
		enemy_bullet_group.add(bullet6)
		enemy_bullet_group.add(bullet7)
		
	def update(self):
		self.rect.y += self.y_vel
		self.move_counter += self.y_vel
        
		if self.move_counter >= self.move_steps:
			self.explode()
			self.kill()

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
        self.move_counter = 0		#aka licznik krokow golembia
        self.move_direction = 1
        self.hp = 1
        self.x_vel = 2				#musi byc Int !!! inaczej sie jebie
        self.y_step = 5			#liczba pikseli kroku w dol

    def update(self):
        self.rect.x += self.x_vel * self.move_direction
        self.move_counter += self.x_vel
        if abs(self.move_counter) > self.move_steps:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
            self.rect.y += self.y_step
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
		self.x_vel = 4				#musi byc Int !!! inaczej sie jebie
		self.y_vel = 4				#oraz parzyste
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

#chonker pigeon
class Pigeon03(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/pigeon_03.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]
		
		self.last_shot = pygame.time.get_ticks()
		
		global ENEMY_COUNTER			#zliczanie przeciwnikow
		ENEMY_COUNTER += 1
		self.move_steps = 100
		self.move_steps_1 = 20
		self.move_counter = 0		#aka licznik krokow obiektu
		self.move_sequence = 0
		self.move_counter_1 = 0
		self.move_sequence_1 = 0
		self.move_direction = 1
		self.hp = 4
		self.x_vel = 1				#musi byc Int !!! inaczej sie jebie
		self.y_vel = 1
		self.y_step = 5			#liczba pikseli kroku w dol
		self.cooldown = 3000		#miliseconds

	def update(self):
		if self.move_sequence == 0:
			self.rect.x += self.x_vel
			self.move_counter += self.x_vel
			if self.move_counter >= self.move_steps:
				self.move_counter = 0
				self.move_sequence = 1
		elif self.move_sequence == 1:
			self.rect.x -= self.x_vel
			self.move_counter += self.x_vel
			if self.move_counter >= self.move_steps:
				self.move_counter = 0
				self.move_sequence = 0
								
		if self.move_sequence_1 == 0:
			self.rect.y += self.y_vel
			self.move_counter_1 += self.y_vel
			if self.move_counter_1 >= self.move_steps_1:
				self.move_counter_1 = 0
				self.move_sequence_1 = 1
		elif self.move_sequence_1 == 1:
			self.rect.y -= self.y_vel
			self.move_counter_1 += self.y_vel
			if self.move_counter_1 >= self.move_steps_1:
				self.move_counter_1 = 0
				self.move_sequence_1 = 0
		
		#record current time
		time_now = pygame.time.get_ticks()
		
		if time_now - self.last_shot > self.cooldown:
			if randint(0, 1) == 0: 
				bullet = Enemy_Egg01(self.rect.centerx, self.rect.bottom, 2, 0)
				enemy_bullet_group.add(bullet)
			self.last_shot = time_now
		
		if pygame.sprite.spritecollide(self, bullet_group, True):
			self.hp -= 1
		if self.hp <= 0:
			self.kill()
			global ENEMY_COUNTER, SCORE
			ENEMY_COUNTER -= 1
			SCORE += 4
