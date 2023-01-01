import classes_game
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


def start():
    global entities, platforms, thorns, coins_list, hero, left, right, up, dagger, coins
    left = right = up = False
    dagger = 0
    coins = 0
    entities = pygame.sprite.Group()
    platforms = []
    thorns = []
    coins_list = []
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == '|':
                th = Thorns(x, y + 19, 0)
                thorns.append(th)
                entities.add(th)
            if col == '<':
                th = Thorns(x + 19, y, 90)
                thorns.append(th)
                entities.add(th)
            if col == 'V':
                th = Thorns(x, y, 180)
                thorns.append(th)
                entities.add(th)
            if col == '>':
                th = Thorns(x, y, 270)
                thorns.append(th)
                entities.add(th)
            if col == '@':
                hero = Hero(x, y)
                entities.add(hero)
            if col == '0':
                coin = Coin(x, y)
                coins_list.append(coin)
                entities.add(coin)
            if col == 'E':
                end = End(x, y)
                entities.add(end)
                thorns.append(end)
            x += pl_WD
        y += pl_HG
        x = 0


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
    level = open_level('game_levels/3_lvl.txt')

    left = right = up = dagger = coins = 0
    entities = platforms = thorns = coins_list = hero = 0
    start()

    running = True

    while running:
        for ev in event.get():
            if ev.type == QUIT:
                running = False
            if ev.type == KEYDOWN and ev.key == K_a:
                left = True
            if ev.type == KEYDOWN and ev.key == K_d:
                right = True
            if ev.type == KEYDOWN and ev.key == K_r:
                start()
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
                if hero in entities:
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
                if hero.live == 0:
                    entities.remove(hero)
                    all_sprites.remove(hero)
                    entities.remove(dagger)
                    dagger = 0
                    hero.live = -1
                if hero in entities:
                    if len(hero.coins) > 0:
                        for coin in hero.coins:
                            entities.remove(coin)
                            all_sprites.remove(coin)
                            coins_list.remove(coin)
                            hero.coins.remove(coin)
                            coins += 1
                    if classes_game.win:
                        entities.remove(hero)
                        all_sprites.remove(hero)
                        entities.remove(dagger)
                        dagger = 0
                        print('Монеты:', coins, 'из', (coins + len(coins_list)))
                    else:
                        hero.update(left, right, up, platforms, thorns, coins_list)
                        if dagger:
                            dagger.update(platforms)
                            if dagger.check == 1:
                                entities.remove(dagger)
                                dagger = 0
        screen.fill((225, 225, 225))
        if hero in entities:
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
