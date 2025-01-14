import math
import random
import time

import pygame
from pygame.sprite import Sprite

class Coin(Sprite):
    def __init__(self,game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.image = pygame.image.load('images/coin.bmp').convert_alpha()
        self.rect = self.image.get_rect()
        self.spawntime = time.time()

        indx = 0
        indy = 0

        self.rect.y = 0
        self.rect.x = 0

        while game.mapreader.map[indy][indx] != 0:

            indy = math.floor(random.random() * len(game.mapreader.map))
            indx = math.floor(random.random() * len(game.mapreader.map[0]))

        self.rect.y = indy * 40
        self.rect.x = indx * 40



