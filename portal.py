import random
import time

import pygame
from pygame.sprite import Sprite

class Portal(Sprite):
    portals = {}
    cds = {}
    CD = 0.5
    def __init__(self,game, key, pos):
        super().__init__()

        if key in Portal.portals:
            Portal.portals[key].append(self)
        else:
            Portal.portals[key] = [self]

        self.game = game
        self.screen = game.screen
        self.key = key
        Portal.cds[key] = 0
        self.index = len(Portal.portals[key])-1
        self.image = pygame.image.load('images/portal.bmp')
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]


    def activate(self, player):

        if Portal.cds[self.key] < time.time():



            aindex = self.index
            while aindex == self.index:
                aindex = round(random.random() * len(Portal.portals[self.key])- 1)

            aportal = Portal.portals[self.key][aindex]

            player.rect.x = aportal.rect.x
            player.rect.y = aportal.rect.y

        Portal.cds[self.key] = time.time() + Portal.CD


