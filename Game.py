import pygame  # 导入pygame库
from pygame.locals import *  # 导入pygame库中的一些常量
from sys import exit  # 导入sys库中的exit函数
from Hero import Hero
from Setting import Setting
from Enemy import Enemy
from random import randint


class Game:

    def __init__(self):
        # 初始化pygame
        pygame.init()

        self.setting = Setting()
        self.offset = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}
        # 初始化游戏
        self.screen = pygame.display.set_mode(self.setting.windows)  # 初始化一个用于显示的窗口
        pygame.display.set_caption('This is my first pygame-program')  # 设置窗口标题
        self.background = pygame.image.load('image/background.jpg')
        self.feiji = pygame.image.load('image/fj.png')
        self.bullet = pygame.image.load('image/bullet.png')
        self.enemy_img = pygame.image.load('image/enemy.png')
        self.gameover_img = pygame.image.load('image/gameover.jpg')
        self.pass_img = pygame.image.load('image/pass.jpg')
        # 创建敌人组
        self.enemy_group = pygame.sprite.Group()
        # 创建击毁敌人组
        self.enemy_down_group = pygame.sprite.Group()
        # 飞机出事位置
        feiji_pos = [(self.setting.windows[0] - self.feiji.get_rect().width) / 2, self.setting.windows[1] - 100]
        # 飞机对象
        self.heros = Hero(self.feiji, feiji_pos)
        # 限制游戏帧数
        self.clock = pygame.time.Clock()
        # 重绘次数
        self.ticks = 0
        # 分数
        self.makes = 0
        # 最高分数
        self.makesMax = 99999

    def startGame(self):

        # 初始化生命值
        self.heros.add_life(self.feiji, 3)

        while True:

            self.ticks += 1
            self.clock.tick(60)
            # 绘制背景
            self.screen.blit(self.background, (0, 0))  # new
            self.screen.blit(self.heros.image, self.heros.rect)  # new
            self.drawText('分数:%d' % self.makes, self.setting.windows[0] - 120, 40)
            # 产生敌机 *****************************************************

            if self.ticks % 30 == 0:
                enemy = Enemy(self.enemy_img,
                              [randint(0, self.setting.windows[0] - self.enemy_img.get_width()),
                               -self.enemy_img.get_height()])

                self.enemy_group.add(enemy)
            # 控制敌机

            self.enemy_group.update()
            # 绘制敌机

            self.enemy_group.draw(self.screen)
            # ************************************************************
            # 检测敌机与子弹的碰撞 *******************************************

            self.enemy_down_group.add(pygame.sprite.groupcollide(self.enemy_group, self.heros.bullets1, True, True))

            for enemy_down in self.enemy_down_group:
                self.enemy_down_group.remove(enemy_down)
                self.makes += 1

            # ************************************************************
            # 判断是否通关
            if self.makes > self.makesMax:
                break

            # 射击
            if self.ticks % 6 == 0:
                self.heros.single_shoot(self.bullet)
            # 控制子弹

            self.heros.bullets1.update()
            self.heros.bullets2.update()
            self.heros.bullets3.update()
            # self.heros.lifeGroup.update()
            # 绘制子弹

            self.heros.bullets1.draw(self.screen)
            self.heros.bullets2.draw(self.screen)
            self.heros.bullets3.draw(self.screen)
            self.heros.lifeGroup.draw(self.screen)

            # 飞机和障碍物是否有碰撞
            enemy_down_list = pygame.sprite.spritecollide(self.heros, self.enemy_group, True)

            if len(enemy_down_list) > 0:  # 不空

                self.enemy_down_group.add(enemy_down_list)

                self.heros.reduce_life()

            # 更新屏幕
            pygame.display.update()

            # 处理游戏退出
            # 从消息队列中循环取
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:

                    if event.key in self.offset:
                        self.offset[event.key] = self.heros.speed
                elif event.type == pygame.KEYUP:

                    if event.key in self.offset:
                        self.offset[event.key] = 0

            self.heros.move(self.offset)

            # 飞机是否被击毁
            if self.heros.is_hit:
                break

        # 跳出主循环

        if self.heros.is_hit:
            self.screen.blit(self.gameover_img, (0, 0))
        else:
            self.screen.blit(self.pass_img, (0, 0))

        # 玩家坠毁后退出游戏

        while True:
            pygame.display.update()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                    exit()

    def drawText(self, text, posx, posy, textHeight=48, fontColor=(0, 0, 0)):
        fontObj = pygame.font.Font('fonts/STLITI.TTF', textHeight)  # 通过字体文件获得字体对象
        textSurfaceObj = fontObj.render(text, True, fontColor)  # 配置要显示的文字
        textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
        textRectObj.center = (posx, posy)  # 设置显示对象的坐标
        self.screen.blit(textSurfaceObj, textRectObj)  # 绘制字
