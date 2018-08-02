# 飞机类
import pygame
from Bullet import Bullet
from Setting import Setting
from Life import Life


class Hero(pygame.sprite.Sprite):

    def __init__(self, img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.borld = Setting().windows
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.init_pos = init_pos
        self.speed = 6
        self.is_hit = False
        self.life = 1
        self.lifeC = []

        # 子弹1的Group
        self.bullets1 = pygame.sprite.Group()
        self.bullets2 = pygame.sprite.Group()
        self.bullets3 = pygame.sprite.Group()
        self.lifeGroup = pygame.sprite.Group()

    def move(self, offset):

        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]

        y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]

        if x < 0:

            self.rect.left = 0
        elif x > self.borld[0] - self.rect.width:

            self.rect.left = self.borld[0] - self.rect.width
        else:

            self.rect.left = x

        if y < 0:

            self.rect.top = 0
        elif y > self.borld[1] - self.rect.height:

            self.rect.top = self.borld[1] - self.rect.height
        else:

            self.rect.top = y

    def single_shoot(self, bullet1_surface):

        bullet1 = Bullet(bullet1_surface, [self.rect.left + 24, self.rect.top - 8])
        bullet2 = Bullet(bullet1_surface, [self.rect.left + 24 - 8, self.rect.top])
        bullet3 = Bullet(bullet1_surface, [self.rect.left + 24 + 8, self.rect.top])

        self.bullets1.add(bullet1)
        self.bullets2.add(bullet2)
        self.bullets3.add(bullet3)

    def add_life(self, life_img, count):

        if count < 3:
            count = 3

        self.life = count
        for num in range(0, count):
            life = Life(life_img, [20 + num * life_img.get_rect().width, 20])

            self.lifeGroup.add(life)

            self.lifeC.append(life)

    def reduce_life(self):

        if self.life > 0:

            self.lifeGroup.remove(self.lifeC[self.life - 1])

            self.life -= 1

            self.re_start()

        else:
            self.is_hit = True

    def re_start(self):
        self.rect.topleft = self.init_pos
