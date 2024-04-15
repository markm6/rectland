import pygame
import random
import math
import utils
from constants import *
from text import TextOptionMenu
import backgrounds.rectangles

clock = pygame.time.Clock()
def startup_menu(screen) -> int:
    menu = TextOptionMenu(BASE_FONT, (255, 255, 255), (255, 100, 100), (20, 20), ["play", "options", "quit"])
    events = pygame.event.get()
    while not utils.check_quit(events):
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        clock.tick(60)
        screen.fill((0, 0, 0))

        # first handle rects moving, shake etc
        backgrounds.rectangles.render_rects(screen)

        # render text & options next
        mouse_clicked = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
        hovered_opt, clicked_opt = menu.get_interacted(mouse_pos, mouse_clicked)
        menu.blit(screen)
        pygame.display.update()

        if clicked_opt is not None:
            return clicked_opt
    return -1


