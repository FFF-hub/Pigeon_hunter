import pygame
from pygame.locals import *
from random import randint

#init vars
TITLE_ = "Space Pigeons"
SCREEN_SIZE = (1200, 720)

# init
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
screen2 = pygame.display.set_mode(SCREEN_SIZE)
screen3 = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(TITLE_)
icon = pygame.image.load('vis/icon.png').convert()
pygame.display.set_icon(icon)
font = pygame.font.SysFont("Liberation mono", 25, True)
font2 = pygame.font.SysFont("Liberation mono", 17, True)
font3 = pygame.font.SysFont("Liberation Mono", 140, True)

#sound channels
channel_0 = pygame.mixer.Channel(0)
channel_1 = pygame.mixer.Channel(1)
channel_2 = pygame.mixer.Channel(2)
channel_3 = pygame.mixer.Channel(3)
channel_4 = pygame.mixer.Channel(4)
channel_5 = pygame.mixer.Channel(5)
channel_6 = pygame.mixer.Channel(6)
channel_7 = pygame.mixer.Channel(7)

#variables
AI_SC_SIZE = (SCREEN_SIZE[0]//10, SCREEN_SIZE[0]//10)

COOLDOWNS = [600, 1 * 1000, 1 * 1000, 1 * 1000]

DIFFICULTY_LEVEL = 3
ENEMY_COUNTER = 0
SCORE = 0
TEXT_SCORE = font.render("SCORE: " + str(SCORE), False, 0xffffffff)
TEXT_COOLDOWNS = font.render("Q W E R", False, 0xffffffff)
TEXT_COOLDOWNS_VAL = font2.render(str(COOLDOWNS[0]//1000) + "  " + str(COOLDOWNS[1]//1000) + "  " + str(COOLDOWNS[2]//1000) + "  " + str(COOLDOWNS[3]//1000), False, 0xffffffff)
TEXT_SCORE_XY = (5, 5)
TEXT_COOLDOWNS_XY = (1080, 680)
TEXT_COOLDOWNS_VAL_XY = (1080, 650)

#sprite groups
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
rocket_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
hp_group = pygame.sprite.Group()
ui_group = pygame.sprite.Group()

########################################################################
#Player stuff
########################################################################
class Player(pygame.sprite.Sprite):
	def __init__(self, name, hp, x_pos, y_pos, vel, cooldowns: int):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/player_01.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]

		self.last_q = pygame.time.get_ticks()
		self.last_w = pygame.time.get_ticks()
		self.last_e = pygame.time.get_ticks()
		self.last_r = pygame.time.get_ticks()
		self.last_collide = pygame.time.get_ticks()
	
		self.channel_0 = pygame.mixer.Channel(0)
		self.channel_1 = pygame.mixer.Channel(1)
		self.channel_2 = pygame.mixer.Channel(2)
		self.channel_3 = pygame.mixer.Channel(3)
		self.channel_4 = pygame.mixer.Channel(4)
		
		self.sound_hp_down = pygame.mixer.Sound("sfx/hp_down.wav")
		self.sound_hp_down.set_volume(0.3)
		self.sound_q = pygame.mixer.Sound("sfx/q.wav")
		self.sound_q.set_volume(0.2)
		self.sound_w = pygame.mixer.Sound("sfx/w.wav")
		self.sound_w.set_volume(0.2)
		self.sound_e = pygame.mixer.Sound("sfx/e.wav")
		self.sound_e.set_volume(0.2)
		self.sound_r = pygame.mixer.Sound("sfx/r.wav")
		self.sound_r.set_volume(0.2)
			
		self.hp = hp
		self.name = name
		self.vel = vel
		self.cooldown_q = cooldowns[0] 	#milliseconds
		self.cooldown_w = cooldowns[1]
		self.cooldown_e = cooldowns[2]
		self.cooldown_r = cooldowns[3]
		self.immunity = 500 			#mil secs
		self.changed = 0
		self.cd_q_remaining = cooldowns[0]
		self.cd_w_remaining = cooldowns[1]
		self.cd_e_remaining = cooldowns[2]
		self.cd_r_remaining = cooldowns[3]

	def extract_data(self):
		return self.name, self.hp, self.vel, [self.cd_q_remaining, self.cd_w_remaining, self.cd_e_remaining, self.cd_r_remaining], self.rect.x, self.rect.y, self.changed
		
	def update_stats(self, hp: int, vel: int, cooldowns: int):
		self.hp = hp
		self.vel = vel
		self.cooldowns = cooldowns
	
	def sound_master(self):
		self.hp = 1
	
        #player movement
	def update(self):
		self.changed = 0
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
		if key[pygame.K_q] and time_now - self.last_q > self.cooldown_q:
			bullet = Bullet01(self.rect.centerx, self.rect.top, 8, 1)
			bullet_group.add(bullet)
			self.channel_1.play(self.sound_q)
			self.last_q = time_now
		if key[pygame.K_w] and time_now - self.last_w > self.cooldown_w:
			laser = Laser01(self.rect.centerx, self.rect.top - 150)
			laser_group.add(laser)
			self.channel_2.play(self.sound_w)
			self.last_w = time_now
		if key[pygame.K_e] and time_now - self.last_e > self.cooldown_e:
			shield = Shield01(self.rect.centerx, self.rect.centery)
			player_group.add(shield)
			self.channel_3.play(self.sound_e)
			self.last_e = time_now
		if key[pygame.K_r] and time_now - self.last_r > self.cooldown_r:
			rocket = Rocket01(self.rect.centerx, self.rect.top)
			rocket_group.add(rocket)
			self.channel_4.play(self.sound_r)
			self.last_r = time_now
		
		#updateing cooldowns
		if self.cooldown_q - (time_now - self.last_q) < 0:
			self.cd_q_remaining = 0
		else:
			self.cd_q_remaining = self.cooldown_q - (time_now - self.last_q)
		
		if self.cooldown_w - (time_now - self.last_w) < 0:
			self.cd_w_remaining = 0
		else:
			self.cd_w_remaining = self.cooldown_w - (time_now - self.last_w)
		
		if self.cooldown_e - (time_now - self.last_e) < 0:
			self.cd_e_remaining = 0
		else:
			self.cd_e_remaining = self.cooldown_e - (time_now - self.last_e)
		
		if self.cooldown_r - (time_now - self.last_r) < 0:
			self.cd_r_remaining = 0
		else:
			self.cd_r_remaining = self.cooldown_r - (time_now - self.last_r)
				
		
		if pygame.sprite.spritecollide(self, enemy_bullet_group, True):
			global DIFFICULTY_LEVEL
			if DIFFICULTY_LEVEL == 3:
				self.hp -= 1
				self.channel_0.play(self.sound_hp_down)
				self.changed = 1
			elif DIFFICULTY_LEVEL == 2 and randint(0, 1) == 0:
				self.hp -= 1
				self.channel_0.play(self.sound_hp_down)
				self.changed = 1
			elif DIFFICULTY_LEVEL == 1 and randint(0, 2) == 0:
				self.hp -= 1
				self.channel_0.play(self.sound_hp_down)
				self.changed = 1
			elif DIFFICULTY_LEVEL == 0 and randint(0, 4) == 0:
				self.hp -= 1
				self.channel_0.play(self.sound_hp_down)
				self.changed = 1
			
		if pygame.sprite.spritecollide(self, enemies_group, False) and time_now - self.last_collide > self.immunity:
			self.last_collide = time_now
			self.hp -= 1
			self.channel_0.play(self.sound_hp_down)
			self.changed = 1
				
		if self.hp <= 0:
			self.kill()
			
class Shield01(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/shield_01.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]
		
		self.hp = 3
		self.vel = 5

	def update(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > -10:
			self.rect.x -= self.vel
		if key[pygame.K_RIGHT] and self.rect.right < SCREEN_SIZE[0] + 5:
			self.rect.x += self.vel
		if key[pygame.K_UP] and self.rect.top > -10:
			self.rect.y -= self.vel
		if key[pygame.K_DOWN] and self.rect.bottom < SCREEN_SIZE[1] + 10 :
			self.rect.y += self.vel
	
		if pygame.sprite.spritecollide(self, enemy_bullet_group, True):
			self.hp -= 1
	
		if self.hp <= 0:
			self.kill()
			
class Bullet01(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, y_vel, x_vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('vis/bullet_01.png').convert()
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
            
class Laser01(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/laser_01.png').convert()
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]
	
		self.spawn_time = pygame.time.get_ticks()
		self.decay_time = 87 * 3			#time for 5 laser dmg ticks
		self.y_vel = -1
	
	def update(self):
		time_now = pygame.time.get_ticks()
		self.rect.y += self.y_vel
        
		if time_now - self.spawn_time > self.decay_time:
			self.kill()

class Shrapnel01(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos, y_vel, x_vel):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/shrapnel_01.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]
		
		self.channel_0 = pygame.mixer.Channel(6)
		
		self.sound_exp = pygame.mixer.Sound("sfx/r_exp_2.wav")
		self.sound_exp.set_volume(0.3)
		
		self.x_vel = x_vel
		self.y_vel = y_vel
		self.move_counter = 0
		self.move_steps = 100

	def explode(self):
		self.channel_0.play(self.sound_exp)
		bullet0 = Shrapnel02(self.rect.centerx, self.rect.centery,  0, 5)
		bullet1 = Shrapnel02(self.rect.centerx, self.rect.centery,  3, 3)
		bullet2 = Shrapnel02(self.rect.centerx, self.rect.centery,  5, 0)
		bullet3 = Shrapnel02(self.rect.centerx, self.rect.centery,  -3, 3)
		bullet4 = Shrapnel02(self.rect.centerx, self.rect.centery,  0, -5)
		bullet5 = Shrapnel02(self.rect.centerx, self.rect.centery,  -3, -3)
		bullet6 = Shrapnel02(self.rect.centerx, self.rect.centery,  -5, 0)
		bullet7 = Shrapnel02(self.rect.centerx, self.rect.centery,  3, -3)
		
		bullet_group.add(bullet0)
		bullet_group.add(bullet1)
		bullet_group.add(bullet2)
		bullet_group.add(bullet3)
		bullet_group.add(bullet4)
		bullet_group.add(bullet5)
		bullet_group.add(bullet6)
		bullet_group.add(bullet7)

	def update(self):
		self.rect.y += self.y_vel
		self.rect.x += self.x_vel
		self.move_counter += abs(self.y_vel) + abs(self.x_vel)
        
		if self.move_counter >= self.move_steps:
			self.explode()
			self.kill()

		if self.rect.bottom > 720 or self.rect.top < 0 or self.rect.right > 1200 or self.rect.left < 0:
			self.kill()
			
class Shrapnel02(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos, y_vel, x_vel):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/shrapnel_02.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]

		self.x_vel = x_vel
		self.y_vel = y_vel
		self.move_counter = 0
		self.move_steps = 200
		
	def explode(self):
		bullet0 = Shrapnel03(self.rect.centerx, self.rect.centery,  0, 3)
		bullet1 = Shrapnel03(self.rect.centerx, self.rect.centery,  1, 1)
		bullet2 = Shrapnel03(self.rect.centerx, self.rect.centery,  3, 0)
		bullet3 = Shrapnel03(self.rect.centerx, self.rect.centery,  -1, 1)
		bullet4 = Shrapnel03(self.rect.centerx, self.rect.centery,  0, -3)
		bullet5 = Shrapnel03(self.rect.centerx, self.rect.centery,  -1, -1)
		bullet6 = Shrapnel03(self.rect.centerx, self.rect.centery,  -3, 0)
		bullet7 = Shrapnel03(self.rect.centerx, self.rect.centery,  1, -1)
		
		bullet_group.add(bullet0)
		bullet_group.add(bullet1)
		bullet_group.add(bullet2)
		bullet_group.add(bullet3)
		bullet_group.add(bullet4)
		bullet_group.add(bullet5)
		bullet_group.add(bullet6)
		bullet_group.add(bullet7)
		
	def update(self):
		self.rect.y += self.y_vel
		self.rect.x += self.x_vel
		self.move_counter += abs(self.y_vel) + abs(self.x_vel)
        
		if self.move_counter >= self.move_steps:
			self.explode()
			self.kill()

		if self.rect.bottom > 720 or self.rect.top < 0 or self.rect.right > 1200 or self.rect.left < 0:
			self.kill()
			
class Shrapnel03(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos, y_vel, x_vel):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/shrapnel_03.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]

		self.x_vel = x_vel
		self.y_vel = y_vel
		self.move_counter = 0
		self.move_steps = 300

	def update(self):
		self.rect.y += self.y_vel
		self.rect.x += self.x_vel
		self.move_counter += abs(self.y_vel) + abs(self.x_vel)
        
		if self.move_counter >= self.move_steps:
			self.kill()

		if self.rect.bottom > 720 or self.rect.top < 0 or self.rect.right > 1200 or self.rect.left < 0:
			self.kill()

class Rocket01(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/rocket_01.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]
		
		self.channel_0 = pygame.mixer.Channel(5)
		
		self.sound_exp = pygame.mixer.Sound("sfx/r_exp.wav")
		self.sound_exp.set_volume(0.4)
	
		self.y_vel_max = 50
		self.y_vel = 1

	def explode(self):
		self.channel_0.play(self.sound_exp)
		bullet0 = Shrapnel01(self.rect.centerx, self.rect.centery,  0, 6)
		bullet1 = Shrapnel01(self.rect.centerx, self.rect.centery,  4, 4)
		bullet2 = Shrapnel01(self.rect.centerx, self.rect.centery,  6, 0)
		bullet3 = Shrapnel01(self.rect.centerx, self.rect.centery,  -4, 4)
		bullet4 = Shrapnel01(self.rect.centerx, self.rect.centery,  0, -6)
		bullet5 = Shrapnel01(self.rect.centerx, self.rect.centery,  -4, -4)
		bullet6 = Shrapnel01(self.rect.centerx, self.rect.centery,  -6, 0)
		bullet7 = Shrapnel01(self.rect.centerx, self.rect.centery,  4, -4)
		
		bullet_group.add(bullet0)
		bullet_group.add(bullet1)
		bullet_group.add(bullet2)
		bullet_group.add(bullet3)
		bullet_group.add(bullet4)
		bullet_group.add(bullet5)
		bullet_group.add(bullet6)
		bullet_group.add(bullet7)
		
		
	def update(self):
		if self.y_vel < self.y_vel_max:
			self.y_vel += 1
		else:
			self.y_vel = self.y_vel_max
			
		if self.rect.y - self.y_vel	> 5:
			self.rect.y -= self.y_vel
		else:
			self.rect.y = 5
		
		if self.rect.bottom < 30 or pygame.sprite.spritecollide(self, enemies_group, False):
			self.explode()
			self.kill()

class GreenBoxUiElement(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/hp.png').convert()
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]
		
		self.x_pos = x_pos
		self.y_pos = y_pos

	def update(self):
		self.rect.x = self.x_pos
		self.rect.y = self.y_pos

class UserInterface(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/UI_scaled.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = [0, 0]
		
		self.last_cd_refresh = pygame.time.get_ticks()
		self.refresh_cd = 1000
		
		self.somethink = 0
		self.x_elem = 0
		self.y_elem = 0
		
		self.player_data = 0
		
	#to jest gówno do wyświetlania HP tymi kafelkami zielonymi, to robi tak, to tak nie powiino być
	def check_player(self, data):
		if data[len(data) - 1] == 1 and data[1] != 0:
			hp_group.empty()
			for each in range(0, data[1]):
				hp_tile = GreenBoxUiElement(60 + self.x_elem * 10, 700 - self.y_elem * 10)
				hp_group.add(hp_tile)
				self.x_elem += 1
				if each == 5 or each == 11 or each == 17 or each == 23 or each == 29 or each == 35 or each == 41:
					self.y_elem += 1
					self.x_elem = 0
				
			self.y_elem = 0
			self.x_elem = 0
					
			self.somethink = 1
		else:
			self.somethink = 0
		
		self.player_data = data
		
	def init(self, data):
		for each in range(0, data[1]):
			hp_tile = GreenBoxUiElement(60 + self.x_elem * 10, 700 - self.y_elem * 10)
			hp_group.add(hp_tile)
			self.x_elem += 1
			if each == 5 or each == 11 or each == 17 or each == 23 or each == 29 or each == 35 or each == 41:
				self.y_elem += 1
				self.x_elem = 0
				
		self.y_elem = 0
		self.x_elem = 0
				
	def update(self):
		self.rect.x = 0
		self.rect.y = 0
		time_now = self.spawn_time = pygame.time.get_ticks()
		global TEXT_SCORE
		global TEXT_COOLDOWNS
		global TEXT_COOLDOWNS_VAL
		TEXT_SCORE = font.render("SCORE: " + str(SCORE), False, 0xffffffff)
		TEXT_COOLDOWNS = font.render("Q W E R", False, 0xffffffff)
		if time_now - self.last_cd_refresh > self.refresh_cd:
			TEXT_COOLDOWNS_VAL = font2.render(str(self.player_data[3][0]//1000) + "  " + str(self.player_data[3][1]//1000) + "  " + str(self.player_data[3][2]//1000) + "  " + str(self.player_data[3][3]//1000), False, 0xffffffff)


########################################################################
Players = [Player('player', 42, int(SCREEN_SIZE[0] / 2),
		   SCREEN_SIZE[1] - 200,
           5, COOLDOWNS)]

ui = UserInterface()
ui_group.add(ui)
ui.init(Players[0].extract_data())

########################################################################
#Enemy stuff
########################################################################
#Bullet02
class Enemy_Bullet01(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, y_vel, x_vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('vis/enemy_bullet_01.png').convert()
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
		self.image = pygame.image.load('vis/enemy_shrapnel_01.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]

		self.x_vel = x_vel
		self.y_vel = y_vel
		self.move_counter = 0
		self.move_steps = 500

	def update(self):
		self.rect.y += self.y_vel
		self.rect.x += self.x_vel
		self.move_counter += abs(self.y_vel) + abs(self.x_vel)
        
		if self.move_counter >= self.move_steps:
			self.kill()

		if self.rect.bottom > 720 or self.rect.top < 0 or self.rect.right > 1200 or self.rect.left < 0:
			self.kill()


#Egg 1
class Enemy_Egg01(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos, y_vel, x_vel):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/enemy_egg_01.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]

		self.move_steps = randint(150, 700)
		self.move_counter = 0
		self.y_vel = y_vel
		self.div = randint(0, 2)

	def explode(self):
		bullet0 = Enemy_Shrapnel01(self.rect.centerx, self.rect.centery,  0, 3)
		bullet1 = Enemy_Shrapnel01(self.rect.centerx, self.rect.centery,  2, 2)
		bullet2 = Enemy_Shrapnel01(self.rect.centerx, self.rect.centery,  3, 0)
		bullet3 = Enemy_Shrapnel01(self.rect.centerx, self.rect.centery,  -2, 2)
		bullet4 = Enemy_Shrapnel01(self.rect.centerx, self.rect.centery,  0, -3)
		bullet5 = Enemy_Shrapnel01(self.rect.centerx, self.rect.centery,  -2, -2)
		bullet6 = Enemy_Shrapnel01(self.rect.centerx, self.rect.centery,  -3, 0)
		bullet7 = Enemy_Shrapnel01(self.rect.centerx, self.rect.centery,  2, -2)
		
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

#black ops bullets
class Enemy_Bullet02(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos, y_vel, x_vel):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/enemy_bullet_02.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]

		self.creation_time = pygame.time.get_ticks()

		self.x_vel = x_vel
		self.y_vel = y_vel

	def update(self):
		self.rect.y += self.y_vel
		self.rect.x += self.x_vel
		
		time_now = pygame.time.get_ticks()
		
		if time_now - self.creation_time > 5000:
			self.kill()

		if self.rect.bottom > 720 or self.rect.top < 0 or self.rect.right > 1200 or self.rect.left < 0:
			self.kill()

#Pigeons
#Default common enemy
class Pigeon01(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('vis/pigeon_01.png').convert_alpha()
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
        global SCREEN_SIZE
        if abs(self.move_counter) > self.move_steps:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
            self.rect.y += self.y_step
        if pygame.sprite.spritecollide(self, bullet_group, True) or self.rect.y > SCREEN_SIZE[1]:
            self.hp -= 1
        if pygame.sprite.spritecollide(self, laser_group, False):
            self.hp -= 2    
        if self.hp <= 0:
            self.kill()
            global ENEMY_COUNTER, SCORE
            ENEMY_COUNTER -= 1
            SCORE += 1

#UFO pigeon
class Pigeon02(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/pigeon_02.png').convert_alpha()
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
		
		if pygame.sprite.spritecollide(self, laser_group, False):
			self.hp -= 2   
		
		if self.hp <= 0:
			self.kill()
			global ENEMY_COUNTER, SCORE
			ENEMY_COUNTER -= 1
			SCORE += 2

#chonker pigeon
class Pigeon03(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/pigeon_03.png').convert_alpha()
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
		
		if pygame.sprite.spritecollide(self, laser_group, False):
			self.hp -= 2   
		
		if self.hp <= 0:
			self.kill()
			global ENEMY_COUNTER, SCORE
			ENEMY_COUNTER -= 1
			SCORE += 4

#black ops pigeon
class Pigeon04(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/pigeon_04.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]
		
		self.last_shot = pygame.time.get_ticks()
		self.last_change = pygame.time.get_ticks()
		
		global ENEMY_COUNTER		#zliczanie przeciwnikow
		ENEMY_COUNTER += 1
		self.hp = 3
		self.x_vel = randint(-5, 5)	#musi byc Int !!! inaczej sie jebie
		self.y_vel = randint(-5, 5)
		self.fire_sequence = 0
		self.bullet_x_v = 0
		self.bullet_y_v = 0
		self.cooldown = 3000		#miliseconds
		self.move_cooldown = 5000
		self.fire_series_time = 100	

	def update(self):
		#movement: border bouncing
		if self.rect.center[0] >= SCREEN_SIZE[0] - 17-5:
			self.x_vel = randint(-5, -1)
		elif self.rect.center[0] <= 17+5:
			self.x_vel = randint(1, 5)
			
		if self.rect.center[1] >= SCREEN_SIZE[1] - 17-5:
			self.y_vel = randint(-5, -1)
		elif self.rect.center[1] <= 17+5:
			self.y_vel = randint(1, 5)
		
		#record current time
		time_now = pygame.time.get_ticks()
		
		if time_now - self.last_change > self.move_cooldown:
			self.x_vel = randint(-5, 5)
			self.y_vel = randint(-5, 5)
			self.move_cooldown = 100 * randint(10, 50)
			self.last_change = time_now
		
		
		self.rect.x += self.x_vel
		self.rect.y += self.y_vel
		
		
		
		if self.rect.y > 720 or self.rect.y < 0 or self.rect.x > 1200 or self.rect.x < 0:
			self.kill()
		
		if time_now - self.last_shot > self.cooldown and self.fire_sequence == 0:
			self.fire_sequence = 1
			
		if self.fire_sequence == 1:
			self.bullet_x_v = (Players[0].rect.centerx - self.rect.centerx)//AI_SC_SIZE[0]
			self.bullet_y_v = (Players[0].rect.centery - self.rect.centery)//AI_SC_SIZE[1]

			bullet01 = Enemy_Bullet02(self.rect.centerx, self.rect.centery,
									self.bullet_y_v, self.bullet_x_v)
			enemy_bullet_group.add(bullet01)
			self.last_shot = time_now
			self.fire_sequence = 2
		elif self.fire_sequence == 2 and time_now - self.last_shot > self.fire_series_time:
			bullet02 = Enemy_Bullet02(self.rect.centerx, self.rect.centery,
									self.bullet_y_v, self.bullet_x_v)
			enemy_bullet_group.add(bullet02)
			self.last_shot = time_now
			self.fire_sequence = 3
		elif self.fire_sequence == 3 and time_now - self.last_shot > self.fire_series_time:
			bullet03 = Enemy_Bullet02(self.rect.centerx, self.rect.centery,
									self.bullet_y_v, self.bullet_x_v)						
			enemy_bullet_group.add(bullet03)
			self.last_shot = time_now
			self.fire_sequence = 0
		
		if pygame.sprite.spritecollide(self, bullet_group, True):
			self.hp -= 1
			
		if pygame.sprite.spritecollide(self, laser_group, False):
			self.hp -= 2   
			
		if self.hp <= 0:
			self.kill()
			global ENEMY_COUNTER, SCORE
			ENEMY_COUNTER -= 1
			SCORE += 6

#megachonker boss 1
class Boss01(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('vis/boss_01.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = [x_pos, y_pos]
		
		self.last_shot = pygame.time.get_ticks()
		self.last_change = pygame.time.get_ticks()
		
		global ENEMY_COUNTER		#zliczanie przeciwnikow
		ENEMY_COUNTER += 1
		self.hp = 100
		self.max_hp = self.hp
		self.x_vel = 3	#musi byc Int !!! inaczej sie jebie
		self.y_vel = 2
		self.faze = 0
		self.m_sequence_0 = 0
		self.m_steps_0 = 800
		self.m_counter = 0
		self.m_sequence_1 = 0
		self.m_steps_1 = 100
		self.m_counter_v = 0
		self.fire_sequence = 0
		self.bullet_x_v = 0
		self.bullet_y_v = 0
		self.cooldown = 1000		#miliseconds
		self.move_cooldown = 5000
		self.fire_series_time = 100	

	def update(self):
		#faze 1
		if self.m_sequence_0 == 0:
			self.rect.x += self.x_vel
			self.m_counter += self.x_vel
			if self.m_counter >= self.m_steps_0:
				self.m_sequence_0 = 1
				self.m_counter = 0
		elif self.m_sequence_0 == 1:
			self.rect.x -= self.x_vel
			self.m_counter += self.x_vel
			if self.m_counter >= self.m_steps_0:
				self.m_sequence_0 = 0
				self.m_counter = 0
		
		if self.hp < self.max_hp // 2:
			self.faze = 1
		
		#faze 2	
		if self.faze == 1:
			if self.m_sequence_1 == 0:
				self.rect.y += self.y_vel
				self.m_counter_v += self.y_vel
				if self.m_counter_v >= self.m_steps_1:
					self.m_sequence_1 = 1
					self.m_counter_v = 0
			elif self.m_sequence_1 == 1:
				self.rect.y -= self.y_vel
				self.m_counter_v += self.y_vel
				if self.m_counter_v >= self.m_steps_1:
					self.m_sequence_1 = 0
					self.m_counter_v = 0
		
		time_now = pygame.time.get_ticks()
		if self.faze == 0:
			if time_now - self.last_shot > self.cooldown and self.fire_sequence == 0:
				self.fire_sequence = 1
			
			if self.fire_sequence == 1:
				self.bullet_x_v = (Players[0].rect.centerx - self.rect.centerx)//AI_SC_SIZE[0]
				self.bullet_y_v = (Players[0].rect.centery - self.rect.centery)//AI_SC_SIZE[1]

				bullet01 = Enemy_Bullet02(self.rect.centerx, self.rect.centery,
										self.bullet_y_v, self.bullet_x_v)
				enemy_bullet_group.add(bullet01)
				self.last_shot = time_now
				self.fire_sequence = 2
			elif self.fire_sequence == 2 and time_now - self.last_shot > self.fire_series_time:
				bullet02 = Enemy_Bullet02(self.rect.centerx, self.rect.centery,
										self.bullet_y_v, self.bullet_x_v)
				enemy_bullet_group.add(bullet02)
				self.last_shot = time_now
				self.fire_sequence = 3
			elif self.fire_sequence == 3 and time_now - self.last_shot > self.fire_series_time:
				bullet03 = Enemy_Bullet02(self.rect.centerx, self.rect.centery,
										self.bullet_y_v, self.bullet_x_v)						
				enemy_bullet_group.add(bullet03)
				self.last_shot = time_now
				self.fire_sequence = 4
			elif self.fire_sequence == 4 and time_now - self.last_shot > self.fire_series_time:
				bullet04 = Enemy_Bullet02(self.rect.centerx, self.rect.centery,
										self.bullet_y_v, self.bullet_x_v)						
				enemy_bullet_group.add(bullet04)
				self.last_shot = time_now
				self.fire_sequence = 5
			elif self.fire_sequence == 5 and time_now - self.last_shot > self.fire_series_time:
				bullet05 = Enemy_Bullet02(self.rect.centerx, self.rect.centery,
										self.bullet_y_v, self.bullet_x_v)						
				enemy_bullet_group.add(bullet05)
				self.last_shot = time_now
				self.fire_sequence = 0
		elif self.faze == 1:
			if time_now - self.last_shot > self.cooldown and self.fire_sequence == 0:
				self.fire_sequence = 1
				self.cooldown = randint(750, 2500)
			
			if self.fire_sequence == 1:
				bullet01 = Enemy_Egg01(self.rect.centerx - 20, self.rect.centery + 45,
										4, 0)
				bullet10 = Enemy_Egg01(self.rect.centerx + 20, self.rect.centery + 45,
										4, 0)
				enemy_bullet_group.add(bullet01, bullet10)
				self.last_shot = time_now
				self.fire_sequence = 2
			elif self.fire_sequence == 2 and time_now - self.last_shot > self.fire_series_time:
				bullet02 = Enemy_Egg01(self.rect.centerx - 20, self.rect.centery + 45,
										3, 0)
				bullet20 = Enemy_Egg01(self.rect.centerx + 20, self.rect.centery + 45,
										3, 0)
				enemy_bullet_group.add(bullet02, bullet20)
				self.last_shot = time_now
				self.fire_sequence = 3
			elif self.fire_sequence == 3 and time_now - self.last_shot > self.fire_series_time:
				bullet03 = Enemy_Egg01(self.rect.centerx - 20, self.rect.centery + 45,
										2, 0)
				bullet30 = Enemy_Egg01(self.rect.centerx + 20, self.rect.centery + 45,
										2, 0)
				enemy_bullet_group.add(bullet03, bullet30)
				self.last_shot = time_now
				self.fire_sequence = 0
			
		
		if pygame.sprite.spritecollide(self, bullet_group, True):
			self.hp -= 1
			
		if pygame.sprite.spritecollide(self, laser_group, False):
			self.hp -= 1   
			
		if self.hp <= 0:
			self.kill()
			global ENEMY_COUNTER, SCORE
			ENEMY_COUNTER -= 1
			SCORE += 6
