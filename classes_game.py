from pygame import *
import pygame
import os

speed = 6
dagger_speed = 11
dagger_way = 300
jump_speed = 15
max_fall_speed = 15
fall_speed = 1

pl_WD = 38
pl_HG = 38
pl_CL = (255, 0, 0)
all_sprites = sprite.Group()
th_WD = 38
th_HG = 19

win = False


def load_image(name, colorkey=None):
    fullname = os.path.join('game_images', name)
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
        sprite.Sprite.__init__(self, all_sprites)
        self.move_x = 0
        self.move_y = 0
        self.dx = 1
        self.double = 0
        self.check = 0
        self.live = 1
        self.start_x = x
        self.start_y = y
        self.coins = []
        self.wall = False
        self.ground = False
        self.air = True
        self.image = load_image('player.png', -1)
        self.rect = self.image.get_rect(left=x, bottom=y)

    def update(self, left, right, up, platforms, thorns, coin_list):
        global fall_speed
        if left:
            self.move_x = -speed
        if right:
            self.move_x = speed
        if up:
            if self.ground:
                self.move_y = -jump_speed
        if self.double == 1 and self.air and self.check == 0:
            self.double = 0
            self.check = 1
            self.move_y = -jump_speed * 0.9
        if not (left or right):
            self.move_x = 0
        if not self.ground and self.move_y <= max_fall_speed and fall_speed != 0:
            self.move_y += fall_speed
        if self.move_x != 0:
            self.dx = 1 if self.move_x > 0 else 0
        if self.air or self.ground:
            fall_speed = 1
            self.wall = False
        self.air = True if not self.ground else False
        self.ground = False
        self.rect.x += self.move_x
        self.collide(self.move_x, 0, platforms, thorns, coin_list)
        self.rect.y += self.move_y
        self.collide(0, self.move_y, platforms, thorns, coin_list)

    def collide(self, move_x, move_y, platforms, thorns, coin_list):
        global fall_speed, coins, win
        for t in thorns:
            if sprite.collide_mask(self, t):
                if type(t) == End:
                    win = True
                else:
                    self.live = 0
        for p in platforms:
            if sprite.collide_rect(self, p):
                if move_x > 0:
                    self.rect.right = p.rect.left
                    self.wall = True
                if move_x < 0:
                    self.rect.left = p.rect.right
                    self.wall = True
                if move_y < 0:
                    self.rect.top = p.rect.bottom
                    self.move_y = 0
                if move_y > 0:
                    self.rect.bottom = p.rect.top
                    self.ground = True
                    self.air = False
                    self.check = 0
                    self.double = 0
                    self.move_y = 0
                if self.air and self.wall and self.move_y >= 0:
                    self.ground = False
                    self.air = False
                    self.move_y = 2
                    fall_speed = 0
                    self.check = 0
        for coin in coin_list:
            if sprite.collide_mask(self, coin):
                if coin not in self.coins:
                    self.coins.append(coin)


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self, all_sprites)
        self.image = Surface((pl_WD, pl_HG))
        self.image.fill(Color(pl_CL))
        self.rect = Rect(x, y, pl_WD, pl_HG)


class Dagger(sprite.Sprite):
    def __init__(self, dx, x, y):
        super().__init__()
        self.dx = dx
        self.check = 0
        self.move_x = 0
        self.start_x = x
        self.image = load_image('dagger_2.png', -1)
        self.image = pygame.transform.flip(self.image, False if dx else True, False)
        if dx:
            self.rect = self.image.get_rect(left=x, centery=y)
        else:
            self.rect = self.image.get_rect(right=x, centery=y)

    def update(self, platforms):
        self.rect.x += dagger_speed if self.dx else -dagger_speed
        self.move_x += dagger_speed
        self.collide(platforms)
        self.way()

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if self.dx == 1:
                    self.rect.right = p.rect.left
                if self.dx == 0:
                    self.rect.left = p.rect.right
                self.check = 1

    def way(self):
        if self.move_x >= dagger_way:
            self.check = 1


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, width, height):
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.height // 2)


class Thorns(sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__(all_sprites)
        self.image = load_image('thorns.png', -1)
        self.image = transform.rotate(self.image, angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(left=x, top=y)


class Coin(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image('coin.png', -1)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(centerx=x + 19, top=y)


class End(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image('end.png', -1)
        self.rect = self.image.get_rect(centerx=x + 3, top=y)
