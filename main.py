import pygame


def change_image(uc):
    global r, l
    if uc == 'r':
        if r == 0:
            r = 1
        else:
            r = 0
    elif uc == 'l':
        if l == 0:
            l = 1
        else:
            l = 0
    load_image(uc)


def load_image(uc):
    global r, l, image, im_r, im_l
    if uc == 'r':
        image = pygame.image.load(im_r[r]).convert_alpha()
    elif uc == 'l':
        image = pygame.image.load(im_l[l]).convert_alpha()


def up():
    global rect, v_start, v, check_y, v_s, r, check_double
    rect.bottom -= v_start
    v_start -= v
    if rect.bottom >= 300:
        check_y = 0
        check_double = 0
        v_start = v_s
        rect.bottom = 300
        screen.fill((0, 0, 0))


def paint(num):
    global col, colors
    col += num
    if col > len(colors):
        col = 1
    elif col < 1:
        col = len(colors)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Двойной прыжок')
    size = width, height = 600, 400
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    colors = {1: (255, 255, 255), 2: (255, 0, 0), 3: (0, 255, 0), 4: (0, 0, 255),
              5: (255, 255, 0), 6: (255, 0, 255), 7: (0, 255, 255)}
    col = 1
    im_r = {0: 'images/block_r.png', 1: 'images/block_r_p.png'}
    im_l = {0: 'images/block_l.png', 1: 'images/block_l_p.png'}

    running = True
    image = pygame.image.load('images/block_r.png').convert_alpha()
    screen.blit(image, (100, 50))
    rect = image.get_rect(centerx=200, bottom=300)

    move = 10
    v = 1
    v_s = 15
    v_start = v_s
    check_y = 0
    check_double = 0

    r, l = 0, 0

    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 20)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MYEVENTTYPE:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_d]:
                    if rect.right < width:
                        rect.right += move
                        load_image('r')
                    else:
                        rect.right = 1
                        paint(1)
                if keys[pygame.K_a]:
                    if rect.left > 0:
                        rect.left -= move
                        load_image('l')
                    else:
                        rect.left = width - 1
                        paint(-1)
                if check_y == 1:
                    up()
                if check_double == 1:
                    if check_y == 1:
                        v_start = v_s
                    up()
                    check_y = 0
            if event.type == pygame.KEYDOWN:
                cd = event.unicode
                if (cd == 'w' or cd == 'ц' or cd == ' ') and check_double == 0:
                    if check_y == 0:
                        check_y = 1
                    elif check_y == 1:
                        check_double = 1
                if cd == 'p' or cd == 'з':
                    paint(1)
                if cd == 'r' or cd == 'к':
                    change_image('r')
                if cd == 'l' or cd == 'д':
                    change_image('l')
        screen.fill((0, 0, 0))
        screen.blit(image, rect)
        pygame.draw.line(screen, colors[col], (0, 300), (width, 300), 1)
        pygame.display.flip()
    pygame.quit()
