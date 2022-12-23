from pygame import *
from classes import *


def open_level(name):
    file = open(name, mode='r')
    lvl = []
    for line in file.readlines():
        lvl.append(line.strip())
    return lvl


if __name__ == '__main__':
    init()
    display.set_caption('Платформер')
    size = width, height = 800, 640
    screen = display.set_mode(size)
    screen.fill((0, 0, 0))

    MYEVENTTYPE = USEREVENT + 1
    time.set_timer(MYEVENTTYPE, 20)

    hero = Hero(57, 595)
    left = right = up = False
    dagger = 0

    level = open_level('levels/1_lvl.txt')

    entities = sprite.Group()
    platforms = []
    entities.add(hero)

    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            x += pl_WD
        y += pl_HG
        x = 0

    running = True

    while running:
        for ev in event.get():
            if ev.type == QUIT:
                running = False
            if ev.type == KEYDOWN and ev.key == K_a:
                left = True
            if ev.type == KEYDOWN and ev.key == K_d:
                right = True
            if ev.type == KEYDOWN and ev.key == K_w:
                up = True
            if ev.type == KEYUP and ev.key == K_w:
                up = False
            if ev.type == KEYUP and ev.key == K_d:
                right = False
            if ev.type == KEYUP and ev.key == K_a:
                left = False
            if ev.type == KEYDOWN and ev.key == K_l:
                if not dagger:
                    dagger = Dagger(hero.dx,
                                    hero.rect.right if hero.dx == 1 else hero.rect.left, hero.rect.centery)
                    entities.add(dagger)
                else:
                    hero.rect.x = dagger.rect.x
                    hero.rect.y = dagger.rect.y
                    dagger.check = 1
                    hero.move_y = 0
            if ev.type == MYEVENTTYPE:
                hero.update(left, right, up, platforms)
                if dagger:
                    dagger.update(platforms)
                    if dagger.check == 1:
                        entities.remove(dagger)
                        dagger = 0
        screen.fill((225, 225, 225))
        entities.draw(screen)
        display.flip()
    quit()