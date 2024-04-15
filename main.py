import pygame
from constants import *
from menus import startup_menu
from gameplay import gameplay_screen

import utils
loading_text = BASE_FONT.render("Loading...", True, (255, 255, 255))

pygame.display.set_caption("operation rectzland (menu)")

while True:
    scr1 = startup_menu(screen)
    if scr1 == -1 or scr1 == 2:
        utils.quit_game()
    elif scr1 == 0:
        scr2 = gameplay_screen()
