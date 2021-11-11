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

class CHARACTER(enumerate):
    AMADOR = 1
    PROFISSIONAL = 2
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self, gameMode):
        super().__init__() 

        self.sprites = []
        
        if gameMode == GAMEMODE.CLASSICO:
            self.sprites = [
                pygame.image.load("resources/enemy/obstacle.png").convert_alpha()
            ]
        else:
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
    def __init__(self, character, pos_x, pos_y, speed):
        super().__init__()
        self.sprites = []

        if character == CHARACTER.AMADOR:
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
        else:
            self.sprites = [
                pygame.image.load("resources/player/second_character/R1.png").convert_alpha(),
                pygame.image.load("resources/player/second_character/R2.png").convert_alpha(),
                pygame.image.load("resources/player/second_character/R3.png").convert_alpha(),
                pygame.image.load("resources/player/second_character/R4.png").convert_alpha(),
                pygame.image.load("resources/player/second_character/R5.png").convert_alpha(),
                pygame.image.load("resources/player/second_character/R6.png").convert_alpha(),
                pygame.image.load("resources/player/second_character/R7.png").convert_alpha(),
                pygame.image.load("resources/player/second_character/R8.png").convert_alpha(),
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
                     choose_character()

            mouse_pos = pygame.mouse.get_pos()
            start_button.draw(mouse_pos, window)

            if not onClick and start_button.is_clicked(mouse_pos, mouse_clicks):
                choose_character()

            pygame.display.update()
            clock.tick(FPS)

def choose_character():
    menuScenery = True
    window.fill(BLACK)
    large_text = MEDIUM_FONT.render("Escolha o personagem", True, YELLOW)
    text_rect = large_text.get_rect()
    text_rect.center = (screen_width // 2, (screen_height // 2) - 50)
    window.blit(large_text, text_rect)
    window.blit(large_text, text_rect)

    
    amador_button = Button("Corredor amador", screen_width // 8.1,
                           screen_height // 2 + 100, 100, 300, YELLOW, BLUE, BLACK, 40)
    profissional_button = Button("Corredor profissional", screen_width // 1.9,
                           screen_height // 2 + 100, 100, 300, YELLOW, BLUE, BLACK, 40)

    while menuScenery:
        mouse_clicks = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            mouse_pos = pygame.mouse.get_pos()

            amador_button.draw(mouse_pos, window)
            profissional_button.draw(mouse_pos, window)

            if amador_button.is_clicked(mouse_pos, mouse_clicks):
                choose_scenary(CHARACTER.AMADOR)
            elif profissional_button.is_clicked(mouse_pos, mouse_clicks):
                choose_scenary(CHARACTER.PROFISSIONAL)

            pygame.display.update()
            clock.tick(FPS)

def choose_scenary(character):
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
                main_game(GAMEMODE.CLASSICO, character)
            elif rua_button.is_clicked(mouse_pos, mouse_clicks):
                main_game(GAMEMODE.RUA, character)
            elif soft_button.is_clicked(mouse_pos, mouse_clicks):
                main_game(GAMEMODE.SOFT, character)

            pygame.display.update()
            clock.tick(FPS)
        
def get_world(gameMode):
    if gameMode == GAMEMODE.CLASSICO:
        return pygame.image.load("resources/background/classico.jpg").convert()
    elif gameMode == GAMEMODE.RUA:
        return pygame.image.load("resources/background/rua.jpg").convert()
    else:
        return pygame.image.load("resources/background/soft.jpg").convert()

def main_game(gameMode, character):
    ENEMY_SPEED = 5
    SCORE = 0
    screen = pygame.display.set_mode(screen_size)
        
    world = get_world(gameMode)
    world_x = 0

    P1 = Player(character, 100,380,0.5)

    #Creating Sprites Groups
    E1 = Enemy(gameMode)
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
 
        # Animação do background
        screen.blit(world, (world_x,0))
        screen.blit(world, (world.get_width() + world_x,0))
        if world_x == -world.get_width():
            screen.blit(world, (world.get_width() + world_x, 0))
            world_x = 0
        world_x-=10
        

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