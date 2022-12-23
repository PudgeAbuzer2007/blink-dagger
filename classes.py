from pygame import *
import pygame
import os
import sys

WD = 24
HG = 38
speed = 7
dagger_speed = 11
dagger_way = 300
jump_speed = 15
max_fall_speed = 15
fall_speed = 1

pl_WD = 32
pl_HG = 32
pl_CL = (255, 0, 0)


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Hero(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.move_x = 0
        self.move_y = 0
        self.dx = 1
        self.start_x = x
        self.start_y = y
        self.ground = False
        self.image = load_image('player.png', -1)
        self.rect = self.image.get_rect(centerx=x, bottom=y)

    def update(self, left, right, up, platforms):
        if left:
            self.move_x = -speed
        if right:
            self.move_x = speed
        if up:
            if self.ground:
                self.move_y = -jump_speed
        if not (left or right):
            self.move_x = 0
        if not self.ground and self.move_y <= max_fall_speed:
            self.move_y += fall_speed
        if self.move_x != 0:
            self.dx = 1 if self.move_x > 0 else 0
        self.ground = False
        self.rect.x += self.move_x
        self.collide(self.move_x, 0, platforms)
        self.rect.y += self.move_y
        self.collide(0, self.move_y, platforms)

    def collide(self, move_x, move_y, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if move_x > 0:
                    self.rect.right = p.rect.left
                if move_x < 0:
                    self.rect.left = p.rect.right
                if move_y < 0:
                    self.rect.top = p.rect.bottom
                    self.move_y = 0
                if move_y > 0:
                    self.rect.bottom = p.rect.top
                    self.ground = True
                    self.move_y = 0


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((pl_WD, pl_HG))
        self.image.fill(Color(pl_CL))
        self.rect = Rect(x, y, pl_WD, pl_HG)


class Dagger(sprite.Sprite):
    def __init__(self, dx, x, y):
        super().__init__()
        self.dx = dx
        self.check = 0
        self.start_x = x
        self.image = load_image('dagger.png', -1)
        self.image = pygame.transform.flip(self.image, False if dx else True, False)
        if dx:
            self.rect = self.image.get_rect(left=x, centery=y)
        else:
            self.rect = self.image.get_rect(right=x, centery=y)

    def update(self, platforms):
        self.rect.x += dagger_speed if self.dx else -dagger_speed
        self.collide(platforms)
        self.way()

    def collide(self, platforms):
        global dagger_speed
        for p in platforms:
            if sprite.collide_rect(self, p):
                if self.dx == 1:
                    self.rect.right = p.rect.left
                if self.dx == 0:
                    self.rect.left = p.rect.right
                self.check = 1

    def way(self):
        if abs(self.start_x - self.rect.x) >= dagger_way:
            self.check = 1
