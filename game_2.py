from pygame import *
from classes_game import *


def open_level(name):
    global level_rows
    file = open(name, mode='r')
    lines = file.readlines()
    lvl = []
    level_rows = len(lines)
    for line in lines:
        lvl.append(line.strip())
    return lvl


width, height = 800, 640
camera = Camera(width, height)

if __name__ == '__main__':
    init()
    display.set_caption('Платформер')
    size = width, height
    screen = display.set_mode(size)
    screen.fill((0, 0, 0))

    MYEVENTTYPE = USEREVENT + 1
    time.set_timer(MYEVENTTYPE, 20)

    level_rows = 0
    level = open_level('game_levels/2_lvl.txt')

    hero = Hero(pl_WD + 25, (level_rows - 1) * pl_HG)
    left = right = up = False
    dagger = 0

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
                if hero.air and hero.double == 0:
                    hero.double = 1
                else:
                    up = True
                if not hero.air:
                    hero.double = 0
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
                    hero.rect.centery = dagger.rect.centery
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
        camera.update(hero)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        if dagger:
            dagger.rect.centery += camera.dy
            dagger.rect.x += camera.dx
        entities.draw(screen)
        display.flip()
    quit()
