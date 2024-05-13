import pygame
from constants import *
from menus import startup_menu, song_menu
from gameplay import gameplay_screen
import time
import utils
import random

loading_text = BASE_FONT.render("Loading...", True, (255, 255, 255))

pygame.display.set_caption("operation rectzland (menu)")

scr = 2

events = pygame.event.get()
curr_chart = None

while not utils.check_quit(events):
    t1 = time.time()
    if scr == 0:
        return_code = startup_menu(events)
        if return_code is not None:
            scr = return_code
    elif scr == 1:
        # TODO: make some charts at home, add a menu here to select between charts
        return_code = song_menu(events)
        if return_code is not None:
            scr = return_code
    elif scr == 2:
        return_code = gameplay_screen(events)
        if return_code is not None:
            scr = return_code
    t2 = time.time()
    events = pygame.event.get()
