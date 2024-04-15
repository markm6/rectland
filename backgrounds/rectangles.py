import random
import math
from constants import *

N_RECTANGLES = 120


def gen_rgb(n):
    r = int((254 * (n / N_RECTANGLES)))
    g = int((127 * (math.sin(n / 30) + 1)))
    b = int(255 - ((n / N_RECTANGLES) * 255))
    return r, g, b


def gen_random_coords() -> tuple[int, int, int, int]:
    x1 = random.randint(0, 5000)
    y1 = random.randint(0, 700)

    return x1, y1, random.randint(100, 300), random.randint(100, 300)


widths = [random.randint(80, 250) for _ in range(N_RECTANGLES)]
rects = [pygame.Rect(*gen_random_coords()) for _ in range(N_RECTANGLES)]
surfs = [pygame.Surface(r.size, pygame.SRCALPHA).convert_alpha() for r in rects]

for i in range(len(surfs)):
    surfs[i].set_alpha(40)
    c = gen_rgb(i)
    surfs[i].fill(c)

colors = [gen_rgb(i) for i in range(N_RECTANGLES)]
initial_x = [r.x for r in rects]


# -------- Main Program Loop -----------

def render_rects(scr):
    global rects
    for r in range(len(rects)):
        rects[r].move_ip(random.randint(-5, -3), random.randint(-1, 1))
        if rects[r].x < -300:
            rects[r].move_ip(random.randint(2000, 8000), 0)
        if rects[r].x < 1500:
            scr.blit(surfs[r], rects[r])
