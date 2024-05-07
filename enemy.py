import pygame
from random import *

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./pictures/enemy1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([ \
            pygame.image.load("./pictures/enemy1_down1.png").convert_alpha(), \
            pygame.image.load("./pictures/enemy1_down2.png").convert_alpha(), \
            pygame.image.load("./pictures/enemy1_down3.png").convert_alpha(), \
            pygame.image.load("./pictures/enemy1_down4.png").convert_alpha()])

        self.rect = self.image.get_rect()       # 获取自身尺寸
        self.width, self.height = bg_size[0], bg_size[1]    # 获取活动范围
        self.speed = 2
        self.alive = True
        self.mask = pygame.mask.from_surface(self.image)

        # 敌机的初始位置
        self.rect.left, self.rect.top = \
            randint(0,self.width - self.rect.width), randint(-5 * self.height, 0)
            # 范围小，生成的会密一些

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    def reset(self):
        self.alive = True
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), randint(-5 * self.height, 0)

class MidEnemy(pygame.sprite.Sprite):
    energy = 8
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./pictures/enemy2.png").convert_alpha()
        self.image_hit = pygame.image.load("./pictures/enemy2_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([ \
            pygame.image.load("./pictures/enemy2_down1.png").convert_alpha(), \
            pygame.image.load("./pictures/enemy2_down2.png").convert_alpha(), \
            pygame.image.load("./pictures/enemy2_down3.png").convert_alpha(), \
            pygame.image.load("./pictures/enemy2_down4.png").convert_alpha()])

        self.rect = self.image.get_rect()       # 获取自身尺寸
        self.width, self.height = bg_size[0], bg_size[1]    # 获取活动范围
        self.speed = 1.2
        self.alive = True
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = MidEnemy.energy
        self.hit = False

        # 敌机的初始位置
        self.rect.left, self.rect.top = \
            randint(0,self.width - self.rect.width), randint(-10 * self.height, -self.height)
            # 范围大点，生成的会少一些，并且保证初始不会出现

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    def reset(self):
        self.alive = True
        self.energy = MidEnemy.energy
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), randint(-10 * self.height, -self.height)

class LargeEnemy(pygame.sprite.Sprite):
    energy = 20
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("./pictures/enemy3_n1.png").convert_alpha()
        self.image2 = pygame.image.load("./pictures/enemy3_n2.png").convert_alpha()
        self.image_hit = pygame.image.load("./pictures/enemy3_hit.png ").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("./pictures/enemy3_down1.png").convert_alpha(),
            pygame.image.load("./pictures/enemy3_down2.png").convert_alpha(),
            pygame.image.load("./pictures/enemy3_down3.png").convert_alpha(),
            pygame.image.load("./pictures/enemy3_down4.png").convert_alpha(),
            pygame.image.load("./pictures/enemy3_down5.png").convert_alpha(),
            pygame.image.load("./pictures/enemy3_down6.png").convert_alpha()])

        self.rect = self.image1.get_rect()       # 获取自身尺寸
        self.width, self.height = bg_size[0], bg_size[1]    # 获取活动范围
        self.speed = 1
        self.alive = True
        self.mask = pygame.mask.from_surface(self.image1)
        self.energy = LargeEnemy.energy
        self.hit = False

        # 敌机的初始位置
        self.rect.left, self.rect.top = \
            randint(0,self.width - self.rect.width), randint(-15 * self.height, -5 * self.height)
            # 范围大点，生成的会少一些，并且保证初始不会出现

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    def reset(self):
        self.alive = True
        self.energy = LargeEnemy.energy
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), randint(-15 * self.height, -5 * self.height)