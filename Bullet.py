# 子弹
import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()

        self.rect.topleft = init_pos
        self.speed = 8

    def update(self):
        self.rect.top -= self.speed

        if self.rect.top < -self.rect.height:
            self.kill()
