import pygame

import results
from constants import *
from menus import startup_menu, song_menu, scores_menu
from gameplay import gameplay_screen
from results import *
import time
import utils
import random
from enums import ScreenEnum

loading_text = BASE_FONT.render("Loading...", True, (255, 255, 255))

pygame.display.set_caption("operation rectzland (menu)")

scr = ScreenEnum.MENU_STARTUP

events = pygame.event.get()
curr_chart = 0
curr_results = None

while not utils.check_quit(events):
    if scr == ScreenEnum.MENU_STARTUP:
        return_code = startup_menu(events)
        if return_code is not None:
            scr = return_code
    elif scr == ScreenEnum.MENU_SONGS:
        # TODO: make some charts at home, add a menu here to select between charts
        return_code = song_menu(events)
        if return_code is not None:
            if return_code != ScreenEnum.MENU_STARTUP:
                scr = ScreenEnum.GAMEPLAY
                curr_chart = return_code - 2
            else:
                scr = ScreenEnum.MENU_STARTUP
    elif scr == ScreenEnum.GAMEPLAY:
        results = gameplay_screen(events, curr_chart)
        if results is not None:
            curr_results = results
            scr = ScreenEnum.RESULTS
    elif scr == ScreenEnum.RESULTS:
        return_code = results_screen(events, curr_results)
        if return_code:
            curr_results = None
            scr = ScreenEnum.MENU_SONGS
    elif scr == ScreenEnum.OPTIONS:
        ...
    elif scr == ScreenEnum.SCORES_LIST:
        return_code = scores_menu(events, False)
        if return_code:
            scr = return_code

    events = pygame.event.get()
