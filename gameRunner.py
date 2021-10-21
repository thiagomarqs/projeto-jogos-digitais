#Jhonatan Felipe do Nascimento, 32091982
#Thiago da Silva, 32090579

import sys, pygame, time, math, glob
assert sys.version_info >= (3,4), 'This script requires at least Python 3.4'

screen_size = (800,600)
FPS = 60
gravity = (0.0, 3.0)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = [
            pygame.image.load("player\R1.png"),
            pygame.image.load("player\R2.png"),
            pygame.image.load("player\R3.png"),
            pygame.image.load("player\R4.png"),
            pygame.image.load("player\R5.png"),
            pygame.image.load("player\R6.png"),
            pygame.image.load("player\R7.png"),
            pygame.image.load("player\R8.png"),
            ]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    # speed deve ser um número menor que 1
    def update(self, speed):
        self.current_sprite += speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]


class World(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.background_images = self.running_images = glob.glob("resources/background/bg*.png")
		self.background_images.sort()
		self.background = []
		w,h = screen_size
		for b in self.background_images:
			img = pygame.image.load(b)
			imgRect = img.get_rect()
			temp = [img,(0,imgRect.height-h,w,imgRect.height-h)]
			self.background.append(temp)
		self.rect = pygame.Rect((0,0,w,h))
		self.image = pygame.Surface(self.rect.size).convert()
		self.image.blit(self.background[0][0], (0,0), self.background[0][1])
		self.image.blit(self.background[1][0], (0,0), self.background[1][1])
		self.image.blit(self.background[2][0], (0,0), self.background[2][1])
		self.image.blit(self.background[3][0], (0,0), self.background[3][1])
	
	def update(self,speed):
		speedx,speedy = speed
		px,py = (0,0)
		w,h = screen_size		
		for i in range(0,len(self.background)):
			b = self.background[i]
			r = b[0].get_rect()
			(x1,y1,x2,y2) = b[1]
			x1 += px
			x2 += px
			y1 += py
			y2 += py
			while x1 < 0:
				x1 += w
				x2 += w
			while x2 > r.width:
				x1 -= w
				x2 -= w
			self.background[i][1] = (x1,y1,x2,y2)
			px += speedx
			py += speedy
		self.image.blit(self.background[0][0], (0,0), self.background[0][1])
		self.image.blit(self.background[1][0], (0,0), self.background[1][1])
		self.image.blit(self.background[2][0], (0,0), self.background[2][1])
		self.image.blit(self.background[3][0], (0,0), self.background[3][1])

def main():
	pygame.init()
	screen = pygame.display.set_mode(screen_size)
	clock = pygame.time.Clock()
        
	world = pygame.sprite.Group()
	world.add(World())

	ground = pygame.image.load("resources/ground.png").convert_alpha()
	
	moving_sprites = pygame.sprite.Group()
	player = Player(100,350)
	moving_sprites.add(player)

	while True:
		clock.tick(FPS)
		screen.fill((0,0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)
			if event.type == pygame.MOUSEMOTION:
				pos = pygame.mouse.get_pos()
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
			if event.type == pygame.KEYDOWN:
				keys = pygame.key.get_pressed()

		world.update((5,0))
		world.draw(screen)
		moving_sprites.draw(screen)
		player.update(1)
		ground.blit(screen, (100,100))
                
		pygame.display.flip()

if __name__ == '__main__':
	main()
