import pygame


def draw():
    global pos, col, colors
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, colors[col], pos, 15)


def up():
    global pos, v_start, v, check_y, v_s
    pos[1] -= v_start
    v_start -= v
    if pos[1] >= 300:
        check_y = 0
        v_start = v_s
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 255, 255), [pos[0], 300], 15)
        pos = [pos[0], 300]


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Жёлтый круг')
    size = width, height = 420, 400
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    colors = {1: (255, 255, 255), 2: (255, 0, 0), 3: (0, 255, 0), 4: (0, 0, 255)}
    col = 1

    running = True
    v = 1
    v_s = 15
    pos = 0
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 20)
    check_y = 0
    x = 3
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill((0, 0, 0))
                pygame.draw.circle(screen, colors[col], [20, 300], 15)
                pos = [20, 300]
                v_start = v_s
            if event.type == MYEVENTTYPE:
                keys = pygame.key.get_pressed()
                if pos != 0:
                    if keys[pygame.K_a] and pos[0] - 18 >= 0:
                        pos[0] -= x
                        if check_y == 1:
                            up()
                    elif keys[pygame.K_d] and pos[0] + 18 <= width:
                        pos[0] += x
                        if check_y == 1:
                            up()
                    elif check_y == 1:
                        up()
                    if check_y == 0:
                        if keys[pygame.K_w]:
                            check_y = 1
                    draw()
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'p':
                    col += 1
                    if col > 4:
                        col = 1
        pygame.draw.line(screen, (255, 0, 0), (0, 315), (420, 315), 1)
        pygame.display.flip()
    pygame.quit()