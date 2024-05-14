import pygame
import random
import math
import utils
from constants import *
from text import TextOptionMenu
import backgrounds.rectangles
from gameplay import *

clock = pygame.time.Clock()


def startup_menu(events):
    menu = TextOptionMenu(BASE_FONT, (255, 255, 255), (255, 100, 100), (20, 20), ["play", "options", "quit"])
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
    if clicked_opt == 0:
        return 1
    elif clicked_opt == 1:
        return 2
    elif clicked_opt == 2:
        utils.quit_game()
    menu.blit(screen)
    pygame.display.update()


curr_chart_playing = None
menu = TextOptionMenu(BASE_FONT, (255, 255, 255), (255, 100, 100), (20, 20),
                      ["level 1: test", "level 2: ...", "level 3: ...", "back"])


def song_menu(events):
    global curr_chart_playing
    # TODO: finish up song menu, make a new background for this
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
    if clicked_opt == 0:
        return 2
    elif clicked_opt == 1:
        return 3
    elif clicked_opt == 2:
        return 4
    elif clicked_opt == 3:
        return 0
