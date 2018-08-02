# 障碍类
import pygame
from Setting import Setting


class Enemy(pygame.sprite.Sprite):

    def __init__(self, img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 2
        self.borld = Setting().windows

    def update(self):
        self.rect.top += self.speed

        if self.rect.top > self.borld[1]:
            self.kill()
