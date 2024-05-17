import pygame

import results
from constants import *
from menus import startup_menu, song_menu
from gameplay import gameplay_screen
from results import *
import time
import utils
import random

loading_text = BASE_FONT.render("Loading...", True, (255, 255, 255))

pygame.display.set_caption("operation rectzland (menu)")

scr = 0

events = pygame.event.get()
curr_chart = 0
curr_results = None

while not utils.check_quit(events):
    if scr == 0:
        return_code = startup_menu(events)
        if return_code is not None:
            scr = return_code
    elif scr == 1:
        # TODO: make some charts at home, add a menu here to select between charts
        return_code = song_menu(events)
        if return_code is not None:
            scr = return_code
            if return_code != 0:
                curr_chart = return_code - 2
    elif scr == 2:
        results = gameplay_screen(events, curr_chart)
        if results is not None:
            curr_results = results
            scr = 3
    elif scr == 3:
        return_code = results_screen(events, curr_results)
        if return_code:
            scr = return_code

    events = pygame.event.get()