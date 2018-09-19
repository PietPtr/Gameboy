import pygame

black = 50, 74, 70
darkgray = 57, 88, 85
lightgray = 78, 104, 83
white = 108, 124, 67

def render(queue):
    pygame.init()

    size = width, height = 160, 144

    screen = pygame.display.set_mode(size)
    screen.fill(black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    zoom *= 1.1
                if event.button == 5:
                    zoom /= 1.1

        lcd = queue.get()
        if lcd == None:
            continue

        screen.fill(black)

        screen.blit(generate_screen(lcd), (0, 0))

        pygame.display.flip()


def generate_screen(lcd):
    pixelmap = {
        0b00: black,
        0b01: lightgray,
        0b10: darkgray,
        0b11: white
    }

    surface = pygame.Surface((160, 144))

    for x in range(160):
        for y in range(144):
            surface.set_at((x, y), pixelmap[lcd[y][x]])

    return surface