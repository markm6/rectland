import random
import math
from constants import *

N_RECTANGLES = 5

def gen_rgb(n):
    r = int((254 * (n / N_RECTANGLES)))
    g = int((128 * (math.sin(n / 30) + 1)))
    b = int(255 - ((n / N_RECTANGLES) * 30))
    return r, g, b


def gen_random_coords() -> tuple[int, int, int, int]:
    w, h = random.randint(100, 600), random.randint(100, 650)
    x1 = random.randint(0, SIZE[0] - w - 50)
    y1 = random.randint(0, SIZE[1] - h - 50)

    return x1, y1, w, h


widths = [random.randint(80, 250) for _ in range(N_RECTANGLES)]
rects = [pygame.Rect(*gen_random_coords()) for _ in range(N_RECTANGLES)]
surfs = [pygame.Surface(r.size, pygame.SRCALPHA).convert_alpha() for r in rects]
directions = [[1, 1] for _ in range (N_RECTANGLES)]

for i in range(len(surfs)):
    surfs[i].set_alpha(30)
    c = gen_rgb(i)
    surfs[i].fill(c)


def render_rects(scr):
    global rects
    for r in range(len(rects)):
        if rects[r].bottomright[0] >= SIZE[0] or rects[r].bottomleft[0] <= 0:
            directions[r][0] *= -1
        if rects[r].bottomright[1] >= SIZE[1] or rects[r].topright[1] <= 0:
            directions[r][1] *= -1
        rects[r].move_ip(directions[r][0], directions[r][1])
        scr.blit(surfs[r], rects[r])
