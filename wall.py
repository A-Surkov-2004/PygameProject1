import random
import time

import pygame
from pygame.sprite import Sprite

class Wall(Sprite):
    def __init__(self,game, x,y):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.image = pygame.image.load('images/wall.bmp')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


        self.rect.x = x
        self.rect.y = y

    def activate(self, player):
        pass


    def draw_wall(self):
        self.screen.blit(self.image,self.rect)
        #pg.draw.rect(self.screen, self.color, self.rect)



