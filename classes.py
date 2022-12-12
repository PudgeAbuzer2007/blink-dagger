from pygame import *


WD = 24
HG = 38
speed = 7
jump_speed = 20
fall_speed = 1


pl_WD = 32
pl_HG = 32
pl_CL = (255, 0, 0)


class Hero(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.move_x = 0
        self.move_y = 0
        self.start_x = x
        self.start_y = y
        self.ground = False
        self.image = image.load('images/player.png').convert_alpha()
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
        if not self.ground:
            self.move_y += fall_speed
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