import pygame

import results
from menus import startup_menu, song_menu, scores_menu, pause_menu
from options import options_menu
from gameplay import gameplay_screen
from results import *
import time
import utils
import random
from enums import ScreenEnum

loading_text = BASE_FONT.render("Loading...", True, (255, 255, 255))

pygame.display.set_caption("squarect")

scr = ScreenEnum.MENU_STARTUP

events = pygame.event.get()
curr_chart = 0
curr_results = None
update_scores = False
while not utils.check_quit(events):
    match scr:
        case ScreenEnum.MENU_STARTUP:
            return_code = startup_menu(events)
            if return_code is not None:
                scr = return_code
        case ScreenEnum.MENU_SONGS:
            # TODO: make some charts at home, add a menu here to select between charts
            return_code = song_menu(events)
            if return_code is not None:
                if return_code != ScreenEnum.MENU_STARTUP:
                    scr = ScreenEnum.GAMEPLAY
                    curr_chart = return_code - 2
                else:
                    scr = ScreenEnum.MENU_STARTUP
        case ScreenEnum.GAMEPLAY:
            ret = gameplay_screen(events, curr_chart)
            if ret is not None:
                if type(ret) == results.Results:
                    curr_results = ret
                    scr = ScreenEnum.RESULTS
                else:
                    scr = ret

        case ScreenEnum.RESULTS:
            return_code = results_screen(events, curr_results)
            if return_code:
                curr_results = None
                scr = ScreenEnum.MENU_SONGS
                update_scores = True
        case ScreenEnum.OPTIONS:
            return_code = options_menu()
            if return_code:
                scr = ScreenEnum.MENU_STARTUP
        case ScreenEnum.SCORES_LIST:
            return_code = scores_menu(events, update_scores)
            if update_scores:
                update_scores = False
            if return_code:
                scr = return_code
        case ScreenEnum.PAUSE:
            return_code = pause_menu(events)
            if return_code:
                scr = return_code

    events = pygame.event.get()
