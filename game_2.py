import classes_game
from classes_game import *
import sys
import cv2


def open_level(name):
    global level_rows
    file = open(f'game_levels/{name}', mode='r')
    lines = file.readlines()
    lvl = []
    level_rows = len(lines)
    for line in lines:
        lvl.append(line.strip())
    return lvl


def start():
    global entities, platforms, thorns, coins_list, hero, left, right, up, dagger, coins, all_sprites, num_coins
    if not mixer.music.get_busy():
        mixer.music.unpause()
    end_channel.stop()
    left = right = up = False
    dagger = 0
    coins = 0
    entities = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
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
                all_sprites.add(pf)
            if col == '|':
                th = Thorns(x, y + 19, 0)
                thorns.append(th)
                entities.add(th)
                all_sprites.add(th)
            if col == '<':
                th = Thorns(x + 19, y, 90)
                thorns.append(th)
                entities.add(th)
                all_sprites.add(th)
            if col == 'V':
                th = Thorns(x, y, 180)
                thorns.append(th)
                entities.add(th)
                all_sprites.add(th)
            if col == '>':
                th = Thorns(x, y, 270)
                thorns.append(th)
                entities.add(th)
                all_sprites.add(th)
            if col == '@':
                hero = Hero(x, y)
                entities.add(hero)
                all_sprites.add(hero)
            if col == '0':
                coin = Coin(x, y)
                coins_list.append(coin)
                entities.add(coin)
                all_sprites.add(coin)
            if col == 'E':
                end = End(x, y)
                entities.add(end)
                thorns.append(end)
                all_sprites.add(end)
            x += pl_WD
        y += pl_HG
        x = 0
    num_coins = len(coins_list)

def terminate():
    pygame.quit()
    sys.exit()


def draw(tx, dx, dy):
    font = pygame.font.Font(None, 50)
    text = font.render(tx, True, (255, 100, 100))
    text_x = width // 2 - text.get_width() // 2 + dx
    text_y = height // 2 - text.get_height() // 2 - dy
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    rect = Rect((text_x - 10, text_y - 10, text_w + 20, text_h + 20))
    pygame.draw.rect(screen, (255, 0, 0), rect, 1)
    return rect


def start_screen():
    screen.fill((0, 0, 0))
    start_rect = draw('Играть', 0, 200)
    quit_rect = draw('Выйти', 0, 100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    channel_sounds.play(mixer.Sound('sounds/button.mp3'))
                    return  # начинаем игру
                if quit_rect.collidepoint(event.pos):
                    channel_sounds.play(mixer.Sound('sounds/button.mp3'))
                    terminate()
        pygame.display.flip()


def win_screen():
    global level_rows, level, level_num, levels
    screen.fill((0, 0, 0))
    level_rect = draw('Уровень пройден', 0, 200)
    result_rect = draw(f'Монеты: {coins} из {(coins + len(coins_list))}', 0, 100)
    quit_rect = draw('Выйти', -450, -(height // 2) + 100)
    next_rect = draw('Вперёд', 440, -(height // 2) + 100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_rect.collidepoint(event.pos):
                    channel_sounds.play(mixer.Sound('sounds/button.mp3'))
                    terminate()
                if next_rect.collidepoint(event.pos):
                    channel_sounds.play(mixer.Sound('sounds/button.mp3'))
                    level_rows = 0
                    level_num += 1
                    if level_num + 1 <= len(levels):
                        level = open_level(levels[level_num])
                        start()
                        return
                    else:
                        end_screen()
        pygame.display.flip()


def end_screen():
    pass


width, height = 1200, 670

if __name__ == '__main__':
    init()
    pygame.mixer.music.load('sounds/Pixel_chad.wav')
    pygame.mixer.music.play()
    video = cv2.VideoCapture("game_images/Pixel_chad.mp4")
    success, video_image = video.read()
    fps = video.get(cv2.CAP_PROP_FPS)
    display.set_caption('Платформер')
    window = pygame.display.set_mode((740, 660))
    clock = pygame.time.Clock()
    run = success
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.unicode == ' ':
                run = False
        success, video_image = video.read()
        if success:
            video_surf = pygame.image.frombuffer(
                video_image.tobytes(), video_image.shape[1::-1], "BGR")
        else:
            run = False
        window.blit(video_surf, (0, 0))
        pygame.display.flip()
    quit()

camera = Camera(width, height)

if __name__ == '__main__':
    init()

    channel_sounds = mixer.Channel(1)
    jump_channel = mixer.Channel(2)
    dagger_channel = mixer.Channel(4)
    end_channel = mixer.Channel(3)

    pygame.mixer.music.load('sounds/fon_1.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()
    pygame.mixer.music.pause()

    display.set_caption('Платформер')
    size = width, height
    screen = display.set_mode(size)
    start_screen()
    screen.fill((0, 0, 0))
    levels = ['1_lvl.txt', '2_lvl.txt', '3_lvl.txt']

    level_rows = 0
    level_num = 0
    level = open_level(levels[level_num])

    left = right = up = dagger = coins = all_sprites = 0
    entities = platforms = thorns = coins_list = hero = num_coins = 0
    start()

    MYEVENTTYPE = USEREVENT + 1
    time.set_timer(MYEVENTTYPE, 20)

    running = True

    while running:
        for ev in pygame.event.get():
            if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                pygame.mixer.music.stop()
                running = False
            if ev.type == KEYDOWN and ev.key == K_a:
                left = True
            if ev.type == KEYDOWN and ev.key == K_d:
                right = True
            if ev.type == KEYDOWN and ev.key == K_r:
                start()
            if ev.type == KEYDOWN and ev.key in [K_w, K_SPACE]:
                if hero.live == 1:
                    if hero.air and hero.double == 0:
                        if hero.check == 0:
                            jump_channel.play(mixer.Sound('sounds/jump.mp3'))
                        hero.double = 1
                    else:
                        up = True
                    if not hero.air:
                        hero.double = 0
                        if not hero.wall:
                            jump_channel.play(mixer.Sound('sounds/jump.mp3'))
            if ev.type == KEYUP and ev.key in [K_w, K_SPACE]:
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
                        dagger_channel.play(mixer.Sound('sounds/dagger_drop.mp3'))
                        entities.add(dagger)
                    else:
                        dagger_channel.play(mixer.Sound('sounds/dagger_tp.mp3'))
                        hero.rect.x = dagger.rect.x
                        hero.rect.centery = dagger.rect.centery
                        dagger.check = 1
                        hero.move_y = 0
            if ev.type == MYEVENTTYPE:
                if hero.live == 0:
                    mixer.music.pause()
                    channel_sounds.play(mixer.Sound('sounds/dead.mp3'))
                    hero.move_y = hero.move_x = 0
                    entities.remove(hero)
                    all_sprites.remove(hero)
                    entities.remove(dagger)
                    dagger = 0
                    hero.live = -1
                if hero in entities:
                    for coin in coins_list:
                        if hero.rect.colliderect(coin):
                            channel_sounds.play(mixer.Sound('sounds/coin.mp3'))
                            entities.remove(coin)
                            all_sprites.remove(coin)
                            coins_list.remove(coin)
                            coins += 1
                    if classes_game.win:
                        mixer.music.pause()
                        channel_sounds.set_volume(0.5)
                        channel_sounds.play(mixer.Sound('sounds/end_level_2.mp3'))
                        channel_sounds.set_volume(1)
                        entities.remove(hero)
                        all_sprites.remove(hero)
                        entities.remove(dagger)
                        dagger = 0
                        classes_game.win = False
                        win_screen()
                    else:
                        hero.update(left, right, up, platforms, thorns)
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