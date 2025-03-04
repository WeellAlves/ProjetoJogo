import pygame
import random

pygame.init()
pygame.mixer.init()

import os
fundo = pygame.image.load(os.path.join(os.getcwd(), 'Jogo', 'img', 'Background.png'))
som_laser = pygame.mixer.Sound(f'{os.getcwd()}\\Jogo\\laser.wav')
som_explodir = pygame.mixer.Sound(f'{os.getcwd()}\\Jogo\\explodir.wav')
som_golpe = pygame.mixer.Sound(f'{os.getcwd()}\\Jogo\\golpe.wav')

explodir_lista = []
for i in range(1,13):
	explodir = pygame.image.load(f'{os.getcwd()}\\Jogo\\efeitos_imgs\\{i}.png')
	explodir_lista.append(explodir)
	  
width = fundo.get_width()
height = fundo.get_height()
window = pygame.display.set_mode((width, height))   
pygame.display.set_caption('Jogo do Wellington - Space Invasion')
run = True
fps = 60
clock = pygame.time.Clock()
score = 0
vida = 100
branco = (255,255,255)
negro = (0,0,0)


def pontos(frame, text, size, x,y):
	font = pygame.font.SysFont('Small Fonts', size, bold=True)
	text_frame = font.render(text, True, branco,negro)
	text_rect = text_frame.get_rect()
	text_rect.midtop = (x,y)
	frame.blit(text_frame, text_rect)

def barra_vida(frame, x,y, nivel):
	longitud = 100
	alto = 20
	fill = int((nivel/100)*longitud)
	border = pygame.Rect(x,y, longitud, alto)
	fill = pygame.Rect(x,y,fill, alto)
	pygame.draw.rect(frame, (255,0,55),fill)
	pygame.draw.rect(frame, negro, border,4)

class Jogador(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load(f'{os.getcwd()}\\Jogo\\img\\pybot2.png').convert_alpha()
		pygame.display.set_icon(self.image)
		self.rect = self.image.get_rect()
		self.rect.centerx = width//2
		self.rect.centery = height-70
		self.velocidade_x = 0
		self.vida = 100

	def update(self):
		self.velocidade_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.velocidade_x = -5
		elif keystate[pygame.K_RIGHT]:
			self.velocidade_x = 5

		self.rect.x += self.velocidade_x
		if self.rect.right > width:
			self.rect.right = width
		elif self.rect.left < 0:
			self.rect.left = 0

	def disparar(self):
		bala = Balas(self.rect.centerx, self.rect.top)
		grupo_jogador.add(bala)
		grupo_balas_jogador.add(bala)
		som_laser.play()

class Inimigos(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		
		self.image = pygame.image.load(f'{os.getcwd()}\\Jogo\\img\\inimigo1.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(2, width-40)
		self.rect.y = 10
		self.velocidade_y = random.randrange(-5,20)

	def update(self):
		self.time = random.randrange(-1, pygame.time.get_ticks()//5000)
		self.rect.x += self.time
		if self.rect.x >= width:
			self.rect.x = 0
			self.rect.y += 50

	def disparar_inimigos(self):
		bala = Balas_inimigos(self.rect.centerx, self.rect.bottom)
		grupo_jogador.add(bala)
		grupo_balas_inimigos.add(bala)
		som_laser.play()

class Balas(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load(f'{os.getcwd()}\\Jogo\\img\\laserBullet.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.y = y
		self.velocidade = -18

	def update(self):
		self.rect.y +=  self.velocidade
		if self.rect.bottom <0:
			self.kill()

class Balas_inimigos(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load(f'{os.getcwd()}\\Jogo\\img\\B1.png').convert_alpha()
		self.image = pygame.transform.rotate(self.image, 180)
		self.rect = self.image.get_rect()
		self.rect.centerx = x 
		self.rect.y = random.randrange(10, width)
		self.velocidade_y = 4

	def update(self):
		self.rect.y +=  self.velocidade_y 
		if self.rect.bottom > height:
			self.kill()

class Explodir(pygame.sprite.Sprite):
	def __init__(self, position):
		super().__init__()
		self.image = explodir_lista[0]	
		img_scala = pygame.transform.scale(self.image, (20,20))	
		self.rect = img_scala.get_rect()
		self.rect.center = position
		self.time = pygame.time.get_ticks()
		self.velocidade_explo = 29
		self.frames = 0 
		
	def update(self):
		tempo = pygame.time.get_ticks()
		if tempo - self.time > self.velocidade_explo:
			self.time = tempo 
			self.frames+=1
			if self.frames == len(explodir_lista):
				self.kill()
			else:
				position = self.rect.center
				self.image = explodir_lista[self.frames]
				self.rect = self.image.get_rect()
				self.rect.center = position

grupo_jogador = pygame.sprite.Group()
grupo_inimigos = pygame.sprite.Group()
grupo_balas_jogador = pygame.sprite.Group()
grupo_balas_inimigos = pygame.sprite.Group()

player = Jogador()
grupo_jogador.add(player)
grupo_balas_jogador.add(player)

for x in range(10):
	inimigo = Inimigos(10,10)
	grupo_inimigos.add(inimigo)
	grupo_jogador.add(inimigo)

while run:
	clock.tick(fps)
	window.blit(fundo, (0,0)) 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print('SAIU')
			run = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.disparar()

	grupo_jogador.update()
	grupo_inimigos.update()
	grupo_balas_jogador.update()
	grupo_balas_inimigos.update() 
	grupo_jogador.draw(window)


	danos = pygame.sprite.groupcollide(grupo_inimigos, grupo_balas_jogador,True,True)
	for i in danos:	
		score+=10
		inimigo.disparar_inimigos()
		inimigo = Inimigos(300,10)
		grupo_inimigos.add(inimigo)
		grupo_jogador.add(inimigo)

		explo = Explodir(i.rect.center)
		grupo_jogador.add(explo)
		som_explodir.set_volume(0.3)		
		som_explodir.play()

	danos2 = pygame.sprite.spritecollide(player, grupo_balas_inimigos, True)
	for j in danos2:
		player.vida -= 10
		if player.vida <=0:
			print('SE FUDEU MANO!!!')
			run = False
		explo1 = Explodir(j.rect.center)
		grupo_jogador.add(explo1)
		som_golpe.play()  

	hits =pygame.sprite.spritecollide(player, grupo_inimigos , False)
	for hit in hits:
		player.vida -= 100 
		inimigos = Inimigos(10,10)
		grupo_jogador.add(inimigos)
		grupo_inimigos.add(inimigos)		
		if player.vida <=0:
			print('GAME OVER')
			run = False

	pontos(window, ('  PONTOS: '+ str(score)+'       '), 30, width-85, 2)
	barra_vida(window, width-285, 0, player.vida)

	pygame.display.flip()
pygame.quit()
