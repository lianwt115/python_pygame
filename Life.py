# 子弹
import pygame


class Life(pygame.sprite.Sprite):

    def __init__(self, img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos

    def update(self):

        self.kill()
