from enum import Enum


class ScreenEnum(Enum):
    """Enum for game state/game screens"""
    MENU_STARTUP = 0
    MENU_SONGS = 1
    GAMEPLAY = 2
    RESULTS = 3
    OPTIONS = 4
    SCORES_LIST = 5
    PAUSE = 6
