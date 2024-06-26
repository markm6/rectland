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
    SCREEN.fill((0, 0, 0))

    # first handle rects moving, shake etc
    backgrounds.rectangles.render_rects(SCREEN)

    # render text & options next
    mouse_clicked = check_mouse_clicked(events)
    hovered_opt, clicked_opt = menu.get_interacted(mouse_pos, mouse_clicked)
    if clicked_opt == 0:
        return ScreenEnum.MENU_SONGS
    elif clicked_opt == 1:
        return ScreenEnum.OPTIONS
    elif clicked_opt == 2:
        return ScreenEnum.SCORES_LIST
    elif clicked_opt == 3:
        utils.quit_game()
    menu.blit(SCREEN)
    pygame.display.update()


curr_chart_playing = None
menu = TextOptionMenu(BASE_FONT, (255, 255, 255), (255, 100, 100), (20, 20),
                      ["level 1: test", "level 2: ...", "level 3: ...", "back"])


def song_menu(events):
    global curr_chart_playing
    # TODO: finish up song menu, make a new background for this
    mouse_pos = pygame.mouse.get_pos()
    clock.tick(60)
    SCREEN.fill((0, 0, 0))

    # first handle rects moving, shake etc
    backgrounds.rectangles.render_rects(SCREEN)

    # render text & options next
    mouse_clicked = check_mouse_clicked(events)
    hovered_opt, clicked_opt = menu.get_interacted(mouse_pos, mouse_clicked)
    menu.blit(SCREEN)
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


# TODO: organization, put scores menu in separate file?
last_scores_text = Text("your last 10 scores:", (30, 30))
scores_f = open("scores/scores.json", "r")
try:
    curr_scores_json = json.load(scores_f)
except json.decoder.JSONDecodeError:
    curr_scores_json = {}
parsed_scores_list = parse_scores_json(curr_scores_json)
sorted_parsed_scores = sorted(parsed_scores_list, key=lambda score_text: score_text.split("on ")[1], reverse=True)
scores_f.close()
scores_list = TextOptionMenu(INFO_FONT, (200, 200, 210), (255, 255, 255), (30, 100), sorted_parsed_scores[:10])



def scores_menu(events, update_scores: bool):
    SCREEN.fill((0, 0, 0))
    backgrounds.squares.render_rects(SCREEN)
    mouse_pos = pygame.mouse.get_pos()
    global scores_f, curr_scores_json, parsed_scores_list, scores_list, sorted_parsed_scores
    if update_scores:
        scores_f = open("scores/scores.json", "r")
        try:
            curr_scores_json = json.load(scores_f)
        except json.decoder.JSONDecodeError:
            curr_scores_json = {}
        parsed_scores_list = parse_scores_json(curr_scores_json)
        sorted_parsed_scores = sorted(parsed_scores_list, key=lambda score_text: score_text.split("on ")[1],
                                      reverse=True)
        scores_f.close()
        scores_list = TextOptionMenu(INFO_FONT, (200, 200, 210), (255, 255, 255), (30, 100), sorted_parsed_scores[:10])

    scores_list.blit(SCREEN)
    last_scores_text.blit(SCREEN)
    exit_menu.blit(SCREEN)
    mouse_clicked = check_mouse_clicked(events)

    hovered_opt, clicked_opt = exit_menu.get_interacted(mouse_pos, mouse_clicked)

    pygame.display.flip()
    if clicked_opt == 0:
        return ScreenEnum.MENU_STARTUP


paused_text = Text("paused", (50, 50), font=BIG_FONT)
back_menu = TextOptionMenu(BASE_FONT, (200, 200, 250), (255, 50, 50), (50, 150), ["resume", "main menu", "quit"])


def pause_menu(events):
    mouse_pos = pygame.mouse.get_pos()
    clicked = check_mouse_clicked(events)
    SCREEN.fill((0, 0, 0))
    paused_text.blit(SCREEN)
    back_menu.blit(SCREEN)
    pygame.display.flip()
    hovered, clicked_opt = back_menu.get_interacted(mouse_pos, clicked)
    if clicked_opt == 0:
        return ScreenEnum.GAMEPLAY
    elif clicked_opt == 1:
        return ScreenEnum.MENU_STARTUP
    elif clicked_opt == 2:
        utils.quit_game()
