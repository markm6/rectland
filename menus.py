import pygame
import random
import math
from utils import check_mouse_clicked
from constants import *
from text import TextOptionMenu, Text
import backgrounds.rectangles, backgrounds.squares
from gameplay import *
import json
from enums import ScreenEnum

clock = pygame.time.Clock()
exit_menu = TextOptionMenu(BASE_FONT, (200, 200, 250), (255, 50, 50), (500, 20), ["exit"])


def startup_menu(events) -> Union[None, ScreenEnum]:
    menu = TextOptionMenu(BASE_FONT, (255, 255, 255), (255, 100, 100), (20, 20),
                          ["play", "options", "scores list", "quit"])
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
        return ScreenEnum.MENU_SONGS
    elif clicked_opt == 1:
        return ScreenEnum.OPTIONS
    elif clicked_opt == 2:
        return ScreenEnum.SCORES_LIST
    elif clicked_opt == 3:
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
    mouse_clicked = check_mouse_clicked(events)
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
        return ScreenEnum.MENU_STARTUP


def parse_scores_json(scores_json: dict) -> list[str]:
    scores = []
    for key in scores_json.keys():
        for score in scores_json[key]:
            scores.append(scores_json[key][score])
    parsed_scores = []
    for score in scores:
        parsed_scores.append(f"{score['chart_name']}: {score['accuracy']}% on {score['date']}")
    return parsed_scores


last_scores_text = Text("your last 10 scores:", (30, 30))
scores_f = open("scores/scores.json", "r")
try:
    curr_scores_json = json.load(scores_f)
except json.decoder.JSONDecodeError:
    curr_scores_json = {}
parsed_scores_list = parse_scores_json(curr_scores_json)
scores_f.close()
scores_list = TextOptionMenu(INFO_FONT, (200, 200, 210), (255, 255, 255), (30, 100), parsed_scores_list)


def scores_menu(events, update_scores: bool):
    screen.fill((0, 0, 0))
    backgrounds.squares.render_rects(screen)
    mouse_pos = pygame.mouse.get_pos()
    global scores_f, curr_scores_json, parsed_scores_list, scores_list
    if update_scores:
        scores_f = open("scores/scores.json", "r")
        curr_scores_json = json.load(scores_f)
        scores_f.close()
        parsed_scores_list = parse_scores_json(curr_scores_json)
        scores_list = TextOptionMenu(INFO_FONT, (200, 200, 210), (255, 255, 255), (30, 100), parsed_scores_list)

    scores_list.blit(screen)
    last_scores_text.blit(screen)
    exit_menu.blit(screen)
    mouse_clicked = check_mouse_clicked(events)

    hovered_opt, clicked_opt = exit_menu.get_interacted(mouse_pos, mouse_clicked)

    pygame.display.flip()
    if clicked_opt == 0:
        return ScreenEnum.MENU_STARTUP
