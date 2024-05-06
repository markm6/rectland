import pygame
from constants import *
from menus import startup_menu
from gameplay import gameplay_screen

import utils
import random

loading_text = BASE_FONT.render("Loading...", True, (255, 255, 255))

pygame.display.set_caption("operation rectzland (menu)")

scr = 0

events = pygame.event.get()
while not utils.check_quit(events):
    if scr == 0:
        return_code = startup_menu(events)
        if return_code:
            scr = return_code
    elif scr == 1:
        return_code = gameplay_screen(events)
        if return_code:
            scr = return_code
    events = pygame.event.get()
