import sys, pygame, math, glob, random, time, pygame.mixer
import pygame
from scoreboard import Scoreboard
from pygame.constants import K_SPACE
from button import Button

pygame.mixer.pre_init(44100, -16, 2, 2048) 

pygame.init()

pygame.mixer.init()

jump_sound = pygame.mixer.Sound('resources/sound/jump.wav')
notification_sound = pygame.mixer.Sound('resources/sound/notification.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
pygame.mixer.music.load('resources/sound/menu.mp3')

pygame.mixer.music.play(-1)

PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 10)
BRONZE = (255, 150, 0)
BLUE = (0, 0, 255)
DARKBLUE = (0, 0, 139)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

screen_width = 800
screen_height = 600
screen_size = (screen_width, screen_height)
window = pygame.display.set_mode(screen_size)

FPS = 20
clock = pygame.time.Clock()

LARGE_FONT = pygame.font.SysFont(None, 115)
MEDIUM_FONT = pygame.font.SysFont(None, 65)
SMALL_FONT = pygame.font.SysFont(None, 35)

scoreboard = Scoreboard(0)

# Tive que passar essa variável como argumento de várias
# funções porque o main_game() não reconheceu essa variável
# como global e não descobri porquê.
is_profissional_unlocked = False

class GAMEMODE(enumerate):
    CLASSICO = 1
    RUA = 2
    SOFT = 3

class CHARACTER(enumerate):
    AMADOR = 1
    PROFISSIONAL = 2

class Enemy(pygame.sprite.Sprite):
    def __init__(self, gameMode, character):
        super().__init__() 

        self.sprites = []
        
        if gameMode == GAMEMODE.CLASSICO:
            self.sprites = [pygame.image.load("resources/enemy/obstacle.png").convert_alpha()]
        else:
            self.sprites = [
                pygame.image.load("resources/enemy/trash.png").convert_alpha(),
                pygame.image.load("resources/enemy/cone.png").convert_alpha(),
                pygame.image.load("resources/enemy/dog.png").convert_alpha(),
                pygame.image.load("resources/enemy/litter.png").convert_alpha(),
                pygame.image.load("resources/enemy/cat.png").convert_alpha(),
                pygame.image.load("resources/enemy/rock.png").convert_alpha(),
            ]

        if character == CHARACTER.AMADOR:
            self.enemy_speed = 0
        elif character == CHARACTER.PROFISSIONAL:
            self.enemy_speed = 10

        self.indexSprite = 0
        self.image = self.sprites[self.indexSprite]
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 490
        self.forceJump = 5
        self.massaJump = 1
        self.type = 1
        self.score = 0
    
    def move(self, speed=None):
        print(self.enemy_speed)
        self.rect.x -= 30 + self.enemy_speed
        self.image = self.sprites[self.indexSprite]
        
        if self.enemy_speed < 40:
            self.enemy_speed += 0.03
        
        if self.rect.x < 0 - 50:
            if(self.indexSprite < len(self.sprites) - 1):
                self.indexSprite += 1
                self.rect = self.image.get_rect()
            else:
                self.indexSprite = 0
            
            # Posicionamento do eixo y de acordo com a imagem
            if self.indexSprite in range(0, 2):
                self.rect.y = 490
            elif(self.indexSprite == 2):
                self.rect.y = 507
            elif(self.indexSprite == 3):
                self.rect.y = 550
            elif(self.indexSprite == 4):
                self.rect.y = 559
            elif(self.indexSprite == 5):
                self.rect.y = 559
            
            self.rect.x = 800 + 50


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

        self.initial_rect_y = self.rect.y

    # speed deve ser um número menor que 1
    def move(self, speed):
        self.current_sprite += speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

    def jump(self):
        if(self.isJump):
            if self.jumpCount >= -10:
                self.rect.y -= (self.jumpCount * abs(self.jumpCount)) * 0.40
                self.jumpCount -= 1
                self.image = self.sprites[0]
            else: 
                self.jumpCount = 10
                self.isJump = False
                self.rect.y = self.initial_rect_y

def game_menu(is_profissional_unlocked, onClick=False):
    menu = True

    window.fill(BLACK)
    large_text = LARGE_FONT.render("Runner Jump", True, YELLOW)
    text_rect = large_text.get_rect()
    text_rect.center = (screen_width // 2, (screen_height // 2) - 50)
    window.blit(large_text, text_rect)
    window.blit(large_text, text_rect)

    start_button = Button("Jogar!", screen_width // 2 - 300,
                          screen_height // 2 + 100, 100, 200, YELLOW, BLUE, BLACK, 40)

    scoreboard_button = Button("Pontuações", screen_width // 2 + 100,
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
                     choose_character(is_profissional_unlocked)

            mouse_pos = pygame.mouse.get_pos()
            start_button.draw(mouse_pos, window)
            scoreboard_button.draw(mouse_pos, window)

            if not onClick and start_button.is_clicked(mouse_pos, mouse_clicks):
                choose_character(is_profissional_unlocked)
            elif not onClick and scoreboard_button.is_clicked(mouse_pos, mouse_clicks):
                show_highscores(is_profissional_unlocked)

            pygame.display.update()
            clock.tick(FPS)

def choose_character(is_profissional_unlocked):
    menuScenery = True
    window.fill(BLACK)
    large_text = MEDIUM_FONT.render("Escolha o personagem", True, YELLOW)
    text_rect = large_text.get_rect()
    text_rect.center = (screen_width // 2, (screen_height // 2) - 50)
    window.blit(large_text, text_rect)
    window.blit(large_text, text_rect)

    character_locked_text = SMALL_FONT.render("'Profissional' bloqueado! Complete 20m!", True, YELLOW)
    character_locked_text_rect = character_locked_text.get_rect()
    character_locked_text_rect.center = (screen_width // 2, (screen_height) - 50)

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
                choose_scenary(CHARACTER.AMADOR, is_profissional_unlocked)
            elif profissional_button.is_clicked(mouse_pos, mouse_clicks) and is_profissional_unlocked == False:
                window.blit(character_locked_text, character_locked_text_rect)
            elif profissional_button.is_clicked(mouse_pos, mouse_clicks):
                choose_scenary(CHARACTER.PROFISSIONAL, is_profissional_unlocked)

            pygame.display.update()
            clock.tick(FPS)

def choose_scenary(character, is_profissional_unlocked):
    menuScenery = True
    window.fill(BLACK)
    large_text = MEDIUM_FONT.render("Escolha o cenário", True, YELLOW)
    text_rect = large_text.get_rect()
    text_rect.center = (screen_width // 2, (screen_height // 2) - 50)
    window.blit(large_text, text_rect)
    window.blit(large_text, text_rect)
    
    classico_button = Button("Classico", screen_width // 2 - 370,
                          screen_height // 2 + 100, 100, 200, YELLOW, BLUE, BLACK, 40)
    rua_button = Button("Rua", screen_width // 2 - 103,
                           screen_height // 2 + 100, 100, 200, YELLOW, BLUE, BLACK, 40)
    soft_button = Button("Soft", screen_width // 2 + 160,
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
                main_game(GAMEMODE.CLASSICO, character, is_profissional_unlocked)
            elif rua_button.is_clicked(mouse_pos, mouse_clicks):
                main_game(GAMEMODE.RUA, character, is_profissional_unlocked)
            elif soft_button.is_clicked(mouse_pos, mouse_clicks):
                main_game(GAMEMODE.SOFT, character, is_profissional_unlocked)

            pygame.display.update()
            clock.tick(FPS)
        
def show_highscores(is_profissional_unlocked, onClick=False):

    window.fill(BLACK)
    large_text = MEDIUM_FONT.render("Highscores", True, YELLOW)
    text_rect = large_text.get_rect()
    text_rect.center = (screen_width // 2, (screen_height // 2) - 230)
    window.blit(large_text, text_rect)

    first_place_text = MEDIUM_FONT.render("1. lugar:   " + str(scoreboard.highscores['first']) + " m", True, GREEN)
    window.blit(first_place_text, ((screen_width // 2) - 150, 150))
    second_place_text = MEDIUM_FONT.render("2. lugar:   " + str(scoreboard.highscores['second']) + " m", True, WHITE)
    window.blit(second_place_text, ((screen_width // 2) - 150, 250))
    third_place_text = MEDIUM_FONT.render("3. lugar:   " + str(scoreboard.highscores['third']) + " m", True, BRONZE)
    window.blit(third_place_text, ((screen_width // 2) - 150, 350))

    back_button = Button("Voltar", screen_width // 2 - 100,
                          screen_height // 2 + 150, 100, 200, YELLOW, BLUE, BLACK, 40)

    while True:
        mouse_clicks = pygame.mouse.get_pressed()
        if onClick and mouse_clicks[0] == 0:
            onClick = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                     game_menu(is_profissional_unlocked)

            mouse_pos = pygame.mouse.get_pos()
            back_button.draw(mouse_pos, window)

            if not onClick and back_button.is_clicked(mouse_pos, mouse_clicks):
                game_menu(is_profissional_unlocked)

            pygame.display.update()
            clock.tick(FPS)

def get_world(gameMode):
    if gameMode == GAMEMODE.CLASSICO:
        return pygame.image.load("resources/background/classico.jpg").convert()
    elif gameMode == GAMEMODE.RUA:
        return pygame.image.load("resources/background/rua.jpg").convert()
    else:
        return pygame.image.load("resources/background/soft.jpg").convert()

def main_game(gameMode, character, is_profissional_unlocked):
    ENEMY_SPEED = 5
    score_temp_count = 0
    screen = pygame.display.set_mode(screen_size)
    display_unlocked_message = False
        
    world = get_world(gameMode)
    world_x = 0

    P1 = Player(character, 100,380,0.5)

    #Creating Sprites Groups
    E1 = Enemy(gameMode, character)
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
                    jump_sound.play()
 
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

        score_temp_count += 0.05
        scoreboard.current_score = int(score_temp_count)
        if scoreboard.current_score >= 20 and is_profissional_unlocked == False:
            is_profissional_unlocked = True
            display_unlocked_message = True
            notification_sound.play()
        else:
            score(scoreboard.current_score)

        if pygame.sprite.spritecollideany(P1, enemies):
            scoreboard.set_new_highscore()
            game_over(is_profissional_unlocked)   
            pygame.display.update()

        if (display_unlocked_message):
            font = pygame.font.Font('freesansbold.ttf', 20)
            unlocked_character_text = font.render("'Profissional' desbloqueado!", True, YELLOW)
            window.blit(unlocked_character_text, (screen_width/2, screen_height/2 * 1.5))

        pygame.display.flip()

def game_over(is_profissional_unlocked):
    game_over_sound.play()
    game_over_text = pygame.font.Font('freesansbold.ttf', 60)
    game_over_text = game_over_text.render("Game Over", True, YELLOW)
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.center = (screen_width // 2, screen_height // 2)
    window.blit(game_over_text, game_over_text_rect)
    pygame.display.flip()
    time.sleep(1)
    game_menu(is_profissional_unlocked)

def score(score):
    font = pygame.font.Font('freesansbold.ttf', 35)
    if scoreboard.is_highscore():
        text = font.render("Score: " + str(score) + " m (highscore)", True, BLUE)
    else:
        text = font.render("Score: " + str(score) + " m", True, WHITE)
    window.blit(text, (0,0))

game_menu(is_profissional_unlocked)