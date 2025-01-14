import math
import time

import pygame as pg
from pygame.sprite import Sprite

DARK_GRAY = (60,60,60)


pg.mixer.init()
shot_sound = pg.mixer.Sound('sounds/shot.flac')
pop_sound = pg.mixer.Sound('sounds/pop2.wav')
boom_sound = pg.mixer.Sound('sounds/boom.wav')

class Bullet(Sprite):

    def __init__(self, game, angle, player):

        super().__init__()
        self.screen = game.screen
        self.color = DARK_GRAY
        self.game = game
        self.timer = 0.1
        self.lsttime = 0
        self.speed = 12
        self.touches_left = 5






        self.sin = math.sin(angle*math.pi/180)
        self.cos = math.cos(angle * math.pi / 180)

        self.image = pg.image.load('images/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx + self.sin * player.rect.width/2 - 1
        self.rect.centery = player.rect.centery + self.cos * player.rect.height/2 - 1


        self.mask = pg.mask.from_surface(self.image)
        self.lastpos = self.rect.center


        shot_sound.play()


    def deal_damage(self, collisions):
        collisions[0].death_timer = collisions[0].respawn_time
        collisions[0].rect.centerx = collisions[0].start_pos[0] * 1000
        collisions[0].rect.centery = collisions[0].start_pos[1] * 1000

    def update(self):
        if self.touches_left == 0:
            self.kill()
        self.lastpos = self.rect.center
        self.rect.y += self.cos * self.speed
        self.rect.x += self.sin * self.speed
        collisions = pg.sprite.spritecollide(self, self.game.walls, False)
        if len(collisions) != 0:

            pop_sound.play()

            pos = collisions[0].rect.center
            bpos = list(self.lastpos)
            self.touches_left -=1

            ind = 0
            while round(abs(bpos[0] - pos[0])) - self.rect.size[0]/2 > round(collisions[0].rect.size[0]/2) or round(abs(bpos[1] - pos[1])) - self.rect.size[1]/2 > round(collisions[0].rect.size[1]/2):
                bpos[1] += self.cos
                bpos[0] += self.sin
                ind += 1
                if ind > 1000:
                    print('Shot clip Error')
                    self.lsttime = time.time()
                    break


            if time.time() - self.lsttime > self.timer:
                if abs(bpos[1]- pos[1]) >= abs(bpos[0] - pos[0]):
                    self.cos *= -1
                else:
                    self.sin *= -1
                self.lsttime = time.time()


        collisions = pg.sprite.spritecollide(self, self.game.players, dokill=False,  collided=pg.sprite.collide_mask)
        if len(collisions) != 0:
            self.deal_damage(collisions)
            boom_sound.play()
            self.kill()









    def draw_bullet(self):
        self.screen.blit(self.image,self.rect)
        #pg.draw.rect(self.screen, self.color, self.rect)
