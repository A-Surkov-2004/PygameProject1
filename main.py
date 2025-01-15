import time

import pygame
import sys

import coin
import player
import portal
from wall import Wall
from mapreader import Mapreader

# Инициализация Pygame
pygame.init()
# Параметры окна

FPS = 30
# Цвета
WHITE = (255, 255, 255)

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GOLD = (255, 150, 0)
GREEN = (0, 255, 0)
# Размеры персонажа и объектов
PLAYER_BORDER_THICKNESS = 2
# Скорость движения персонажа
# Инициализация окна
pygame.display.set_caption("Tunks")
clock = pygame.time.Clock()

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

coin_sound = pygame.mixer.Sound('sounds/coin2.wav')
win_sound = pygame.mixer.Sound('sounds/powerup.wav')
music = pygame.mixer.Sound('sounds/cannontube.ogg')
music.set_volume(0.5)



class Game:

    def __init__(self):
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        self.running = True
        self.music_on = True
        music.play(100)

        self.lvl_timer = 5_400 # кадров



        input_schema2 = player.InputSchema(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT)
        input_schema1 = player.InputSchema(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_f)

        self.players = pygame.sprite.Group()
        p1im = pygame.transform.smoothscale(pygame.image.load('images/Green Tunk.png'), (42,64))
        p1 = player.Player(self, input_schema1, p1im, (80,80))
        self.players.add(p1)
        p2im = pygame.transform.smoothscale(pygame.image.load('images/Red Tank 2.png'), (42,64))
        p2 = player.Player(self, input_schema2, p2im, (self.width - 160,self.height - 160))
        self.players.add(p2)

        self.coins = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.lstcoin = 0
        self.walls = pygame.sprite.Group()
        self.mapreader = Mapreader(self)
        self.mapreader.image2list()
        self.mapreader.generate_map()

        portal1 = portal.Portal(self, 'p1', (400, self.height/2-20))
        self.portals.add(portal1)
        portal2 = portal.Portal(self, 'p1', (self.width-450, self.height/2-20))
        self.portals.add(portal2)

        coin1 = coin.Coin(self)
        self.coins.add(coin1)

        self.mode = 'coin_race'
        self.coins_draw = pygame.image.load('images/Draw.png')
        self.coins_green_win = pygame.image.load('images/Green_Winpng.png')
        self.coins_red_win = pygame.image.load('images/Red_Winpng.png')
        self.start_screen1 = pygame.image.load('images/Start.png')
        self.start_screen2 = pygame.image.load('images/Start2.png')
        self.screen_num = 1









    def run(self):


        while self.screen_num < 3:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.screen_num += 1

            if self.screen_num == 1:
                rect = self.start_screen1.get_rect()
                self.screen.blit(self.start_screen1, rect)
            else:
                rect = self.start_screen2.get_rect()
                self.screen.blit(self.start_screen2, rect)

            pygame.display.flip()
            clock.tick(30)



        # Основной игровой цикл
        while self.running:

            if self.lvl_timer > 0:

                self.lvl_timer -= 1

            else:
                self.running = False

            self.check_events()
            for i in self.players:
                i.control()
            self._update_coins()
            self._update_portals()

            self.draw()

        win_sound.play()

        while True:
            self.end_game()
            self.check_events()



    def end_game(self):

        if game.mode == 'coin_race':
            if self.players.sprites()[0].coins > self.players.sprites()[1].coins:
                rect = self.coins_green_win.get_rect()
                self.screen.blit(self.coins_green_win, rect)
            elif self.players.sprites()[0].coins < self.players.sprites()[1].coins:
                    rect = self.coins_red_win.get_rect()
                    self.screen.blit(self.coins_red_win, rect)
            else:
                    rect = self.coins_draw.get_rect()
                    self.screen.blit(self.coins_draw, rect)

            pygame.display.flip()
            clock.tick(30)



    def _update_coins(self):
        collisions = pygame.sprite.groupcollide(self.players, self.coins, False, True)
        if len(collisions) != 0:
            list(collisions.keys())[0].coins += 1
            coin_sound.play()
            coin1 = coin.Coin(self)

            self.coins.add(coin1)


    def _update_portals(self):
        collisions = pygame.sprite.groupcollide(self.players, self.portals, False, False)
        if len(collisions) != 0:
            list(collisions.values())[0][0].activate(list(collisions.keys())[0])



    def check_events(self):

        keys = pygame.key.get_pressed()

        for i in self.players:
            i.detect_inputs()


        if keys[pygame.K_ESCAPE]:
            pygame.quit()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if self.music_on:
                        self.music_on = False
                        music.stop()
                    else:
                        self.music_on = True
                        music.play(100)

    def draw(self):
            # Рендеринг объектов
            self.screen.fill(WHITE)

            self.coins.draw(self.screen)
            self.portals.draw(self.screen)
            for i in self.players:
                i.blitme()
                for bullet in i.bullets.sprites():
                    bullet.draw_bullet()
            for wall in self.walls.sprites():
                wall.draw_wall()

            # Обновление экрана

            self.display_UI()

            pygame.display.flip()
            clock.tick(FPS)



    def display_UI(self):
        f1size = 25
        f1 = pygame.font.Font(None, f1size)
        text1 = f1.render(f'Coins: {self.players.sprites()[0].coins}     Respawn time: {self.players.sprites()[0].death_timer}', True,
                          GOLD)
        self.screen.blit(text1, (40, 10))

        text2 = f1.render(f'Coins: {self.players.sprites()[1].coins}     Respawn time: {self.players.sprites()[1].death_timer}', True,
                          GOLD)
        text_rect = text2.get_rect()
        text_rect.topright = (self.width-40, 10)
        self.screen.blit(text2, text_rect)

        text3 = f1.render(f'Time: {self.lvl_timer//30//60}:{self.lvl_timer // 30 % 60}', True,
                          GOLD)
        text_rect = text3.get_rect()
        text_rect.center = (self.width/2, 10)
        self.screen.blit(text3, text_rect)





game = Game()
game.run()