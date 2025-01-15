import math
import random
import time
COOLDOWN = 1

import pygame
import pygame as pg
from pygame.sprite import Sprite
import bullet
from collections import deque


class InputSchema():
    def __init__(self,left, right, forward, back, fire):
        self.left = left
        self.right = right
        self.forward = forward
        self.back = back
        self.fire = fire

class MoveInfo():
    def __init__(self,angle, center, image, mask):
        self.angle = angle
        self.center = center
        self.image = image
        self.mask = mask


class Player(Sprite):
    def __init__(self,game, input_schema, image, pos):
        super().__init__()
        self.start_pos = pos
        self.game = game
        self.screen = game.screen
        self.player_velocity = [0, 0]  # Скорость по X и Y
        self.og_image = image.convert_alpha()
        self.mask = pygame.mask.from_surface(self.og_image)
        self.image = self.og_image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.size = self.rect.width
        self.coins = 0
        self.rotSpeed = 6
        self.angle = 0
        self.speed = 6
        self.lastshot = 0
        self.bullets = pg.sprite.Group()
        self.max_bullets = 3
        self.lastrect = self.rect
        self.lastc = self.rect.center
        self.lastimg = self.image
        self.lastangle = self.angle
        self.clipping = False
        self.origRect = self.rect
        self.lmask = self.mask
        self.input_schema = input_schema
        self.moves_record = deque()
        self.death_timer = 0      # frames
        self.respawn_time = 150  # frames




    def rot(self, change_angle):

        self.record_moves()


        self.image = pygame.transform.rotate(self.og_image, self.angle)

        self.angle += change_angle
        self.angle = self.angle % 360

        self.rect = self.image.get_rect(center=self.rect.center)

        self.mask = pygame.mask.from_surface(self.image)
        self.check_wallclip()

        self.load_moves()


    def rotater(self):
        self.rot(-self.rotSpeed)

    def rotatel(self):
        self.rot(self.rotSpeed)

    def gof(self):
        self.go(1)

    def gob(self):
        self.go(-1)

    def go(self, direction):

        self.record_moves()

        self.rect.y += math.cos(self.angle*math.pi/180)*self.speed*direction
        self.rect.x += math.sin(self.angle*math.pi/180)*self.speed*direction
        self.check_wallclip()

        self.load_moves()





    def record_moves(self):
        if not self.clipping:
            self.moves_record.append(MoveInfo(self.angle, self.rect.center, self.image, self.mask))
        if len(list(self.moves_record)) > 10:
            self.moves_record.popleft()

    def load_moves(self):
        if self.clipping:
            if len(self.moves_record) != 0:
                data = self.moves_record.pop()
                self.angle = data.angle
                self.rect.center = data.center
                self.image = data.image
                self.mask = data.mask


    def control(self):
        if self.death_timer > 0:
            self.death_timer -= 1
            if self.death_timer == 0:
                self.respawn()
        self.check_wallclip()
        self.update_bullets()
        self.blitme()

    def respawn(self):
        self.rect.centerx = self.start_pos[0]
        self.rect.centery = self.start_pos[1]

    def blitme(self):
            self.screen.blit(self.image, self.rect)

    def check_cooldown(self):
        if not (time.time() - self.lastshot < COOLDOWN):
            self.lastshot = time.time()
            return True
        else:
            return False

    def fire_bullet(self):
        if len(self.bullets) < self.max_bullets:
            new_bullet = bullet.Bullet(self.game, self.angle, self)
            self.bullets.add(new_bullet)

    def update_bullets(self):
        for bullet in self.bullets.copy():
            bullet.update()
            if bullet.rect.bottom <= 0 or bullet.rect.top > self.game.height or bullet.rect.left <= 0 or bullet.rect.right >= self.game.width:
                self.bullets.remove(bullet)

    def check_wallclip(self):
        collisions = pg.sprite.spritecollide(self, self.game.walls, False, collided=pygame.sprite.collide_mask)
        if len(collisions) != 0:
            self.clipping = True
        else:
            self.clipping = False

        othplayers = self.game.players.copy()
        othplayers.remove(self)
        collisions = pg.sprite.spritecollide(self, othplayers, False, collided=pygame.sprite.collide_mask)
        if len(collisions) != 0:
            self.clipping = True

    def detect_inputs(self):
        keys = pygame.key.get_pressed()
        self.change_angle = 0
        if keys[self.input_schema.left]:
            self.rotatel()
        if keys[self.input_schema.right]:
            self.rotater()
        if keys[self.input_schema.forward]:
            self.gof()
        if keys[self.input_schema.back]:
            self.gob()
        if keys[self.input_schema.fire] and self.check_cooldown():
            self.fire_bullet()



