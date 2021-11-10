import sys, pygame, math, glob, random, time, pygame.mixer
import pygame
from pygame.constants import K_SPACE
from button import Button
assert sys.version_info >= (3,4), 'This script requires at least Python 3.4'


pygame.mixer.pre_init(44100, -16, 2, 2048) 

pygame.init()

pygame.mixer.init()

#pygame.mixer.music.load('menu.mp3')

#pygame.mixer.music.play(-1)

PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
DARKBLUE = (0, 0, 139)

screen_width = 800
screen_height = 600
screen_size = (screen_width, screen_height)
window = pygame.display.set_mode(screen_size)

FPS = 20
clock = pygame.time.Clock()

LARGE_FONT = pygame.font.SysFont(None, 115)
MEDIUM_FONT = pygame.font.SysFont(None, 65)

SCORE = 0
ENEMY_SPEED = 5

class GAMEMODE(enumerate):
    CLASSICO = 1
    RUA = 2
    SOFT = 3
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.sprites = [
            pygame.image.load("resources/enemy/trash.png").convert_alpha(),
            pygame.image.load("resources/enemy/cone.png").convert_alpha(),
            pygame.image.load("resources/enemy/dog.png").convert_alpha(),
            pygame.image.load("resources/enemy/litter.png").convert_alpha(),
            pygame.image.load("resources/enemy/cat.png").convert_alpha(),
            pygame.image.load("resources/enemy/rock.png").convert_alpha(),
        ]
        self.indexSprite = 0
        self.image = self.sprites[self.indexSprite]
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 490
        self.forceJump = 5
        self.massaJump = 1
        self.type = 1
        self.score = 0
    
    def move(self, speed):
        self.rect.x -= 45
        if self.rect.x < -500:

            if(self.indexSprite < len(self.sprites) - 1):
                self.indexSprite += 1
            else:
                self.indexSprite = 0
            
            if(self.indexSprite == 0):
                self.rect.x = 800
                self.rect.y = 490

            elif(self.indexSprite == 1):
                self.rect.x = 800
                self.rect.y = 495

            elif(self.indexSprite == 2):
                self.rect.x = 800
                self.rect.y = 507

            elif(self.indexSprite == 3):
                self.rect.x = 800
                self.rect.y = 550
            
            elif(self.indexSprite == 4):
                self.rect.x = 800
                self.rect.y = 559

            elif(self.indexSprite == 5):
                self.rect.x = 800
                self.rect.y = 559
                self.score += 10
            
            self.image = self.sprites[self.indexSprite]
            print(self.score)

    def get_score(self):
        return self.score

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed):
        super().__init__()
        self.sprites = [
            pygame.image.load("resources/player\R1.png").convert_alpha(),
            pygame.image.load("resources/player\R2.png").convert_alpha(),
            pygame.image.load("resources/player\R3.png").convert_alpha(),
            pygame.image.load("resources/player\R4.png").convert_alpha(),
            pygame.image.load("resources/player\R5.png").convert_alpha(),
            pygame.image.load("resources/player\R6.png").convert_alpha(),
            pygame.image.load("resources/player\R7.png").convert_alpha(),
            pygame.image.load("resources/player\R8.png").convert_alpha(),
            ]
        self.current_sprite = 0
        self.jumping = False
        self.jumpheight = 250
        self.anim_air = False
        self.speed = speed

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.isJump = False
        self.jumpCount = 10
        self.type = 2

    # speed deve ser um número menor que 1
    def move(self, speed):
        self.current_sprite += speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

    def jump(self):
        if(self.isJump):
            if self.jumpCount >= -10:
                self.rect.y -= (self.jumpCount * abs(self.jumpCount)) * 0.35
                self.jumpCount -= 1
            else: 
                self.jumpCount = 10
                self.isJump = False

'''
class World(pygame.sprite.Sprite):
    def __init__(self, gameMode):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        
        self.gameMode = gameMode 
        if self.gameMode == GAMEMODE.CLASSICO:
            self.backgroundImages = self.runningImages = glob.glob("resources/background/classico*.png")
        elif self.gameMode == GAMEMODE.RUA:
            self.backgroundImages = self.runningImages = glob.glob("resources/background/rua*.png")
        elif self.gameMode == GAMEMODE.SOFT:
            self.backgroundImages = self.runningImages = glob.glob("resources/background/soft*.png")
        
        self.backgroundImages.sort()
        self.background = []
        w, h = screen_size
        for background in self.backgroundImages:
            img = pygame.image.load(background)
            imgRect = img.get_rect()
            temp = [img,(0,imgRect.height-h,w,imgRect.height-h)]
            self.background.append(temp)

        self.rect = pygame.Rect(0,0,w,h)
        self.image = pygame.Surface(self.rect.size).convert_alpha()

        self.image.blit(self.background[0][0], (0,0), self.background[0][1])
        self.image.blit(self.background[1][0], (0,0), self.background[1][1])
        self.image.blit(self.background[2][0], (0,0), self.background[2][1])
        self.image.blit(self.background[3][0], (0,0), self.background[3][1])
    
    def update(self, speed):
        
        speedx,speedy = speed
        px,py = (0,0)
        w,h = screen_size	
        for background in range(0, len(self.background)):
            b = self.background[background]
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
            self.background[background][1] = (x1,y1,x2,y2)
            px += speedx
            py += speedy
            
            self.image.blit(self.background[0][0], (0,0), self.background[0][1])
            self.image.blit(self.background[1][0], (0,0), self.background[1][1])
            self.image.blit(self.background[2][0], (0,0), self.background[2][1])
            self.image.blit(self.background[3][0], (0,0), self.background[3][1])

'''
def game_menu(onClick=False):


    menu = True

    window.fill(BLACK)
    large_text = LARGE_FONT.render("Runner Jump", True, YELLOW)
    text_rect = large_text.get_rect()
    text_rect.center = (screen_width // 2, (screen_height // 2) - 50)
    window.blit(large_text, text_rect)
    window.blit(large_text, text_rect)

    start_button = Button("Jogar!", screen_width // 2 - 125,
                          screen_height // 2 + 100, 100, 200, YELLOW, BLUE, BLACK, 40)

    while menu:
        mouse_clicks = pygame.mouse.get_pressed()
        if onClick and mouse_clicks[0] == 0:
            onClick = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE:
                     choose_scenary()

            mouse_pos = pygame.mouse.get_pos()
            start_button.draw(mouse_pos, window)

            if not onClick and start_button.is_clicked(mouse_pos, mouse_clicks):
                choose_scenary()

            pygame.display.update()
            clock.tick(FPS)

def choose_scenary():
    menuScenery = True
    window.fill(BLACK)
    large_text = MEDIUM_FONT.render("Escolha o cenário", True, YELLOW)
    text_rect = large_text.get_rect()
    text_rect.center = (screen_width // 2, (screen_height // 2) - 50)
    window.blit(large_text, text_rect)
    window.blit(large_text, text_rect)

    
    classico_button = Button("Classico", screen_width // 2 + 160,
                           screen_height // 2 + 100, 100, 200, YELLOW, BLUE, BLACK, 40)
    rua_button = Button("Rua", screen_width // 2 - 103,
                           screen_height // 2 + 100, 100, 200, YELLOW, BLUE, BLACK, 40)
    soft_button = Button("Soft", screen_width // 2 - 370,
                          screen_height // 2 + 100, 100, 200, YELLOW, BLUE, BLACK, 40)

    while menuScenery:
        mouse_clicks = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            mouse_pos = pygame.mouse.get_pos()

            classico_button.draw(mouse_pos, window)
            rua_button.draw(mouse_pos, window)
            soft_button.draw(mouse_pos, window)

            if classico_button.is_clicked(mouse_pos, mouse_clicks):
                main_game(GAMEMODE.CLASSICO)
            elif rua_button.is_clicked(mouse_pos, mouse_clicks):
                main_game(GAMEMODE.RUA)
            elif soft_button.is_clicked(mouse_pos, mouse_clicks):
                main_game(GAMEMODE.SOFT)

            pygame.display.update()
            clock.tick(FPS)
        
def get_world(gameMode):
    if gameMode == GAMEMODE.CLASSICO:
        return pygame.image.load("resources/background/classico.jpg").convert()
    elif gameMode == GAMEMODE.RUA:
        return pygame.image.load("resources/background/rua.jpg").convert()
    else:
        return pygame.image.load("resources/background/soft.jpg").convert()

def main_game(gameMode):
    ENEMY_SPEED = 5
    SCORE = 0
    screen = pygame.display.set_mode(screen_size)
        
    world = get_world(gameMode)

    P1 = Player(100,380,0.5)

    #Creating Sprites Groups
    E1 = Enemy()
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)

    while True:
        keys = pygame.key.get_pressed()
        clock.tick(FPS)
        screen.fill((0,0,0))
        events = pygame.event.get()

        for event in events:
               
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    P1.isJump = True
 
        #world.update((5,0))
        screen.blit(world, dest=(0,0))
        
        #Moves and Re-draws all Sprites
        for entity in all_sprites:
            window.blit(entity.image, entity.rect)
            entity.move(1)
        
        P1.jump()
        SCORE = E1.get_score()
        score(SCORE)

        if pygame.sprite.spritecollideany(P1, enemies):
            game_over()   
            pygame.display.update()

        pygame.display.flip()

def game_over():
        #pygame.mixer.music.load('game_over.wav')
    #pygame.mixer.music.play()
    #pygame.mixer.music.set_volume(0.5)
    game_over_text = pygame.font.Font('freesansbold.ttf', 60)
    game_over_text = game_over_text.render("Game Over", True, YELLOW)
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.center = (screen_width // 2, screen_height // 2)
    window.blit(game_over_text, game_over_text_rect)
    pygame.display.flip()
    time.sleep(1)
    game_menu()

def score(score):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Score: " + str(score) + " m", True, YELLOW)
    window.blit(text, (0,0))

game_menu()