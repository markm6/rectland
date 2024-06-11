import pygame


def check_quit(events):
    return pygame.event.Event(256) in events


def clamp(val, min_val, max_val):
    v = val
    if val > max_val:
        v = max_val
    elif val < min_val:
        v = min_val
    return v


def quit_game():
    pygame.quit()
    exit(0)


def single_deviation_acc(deviation: float):
    dev = abs(deviation)
    if dev < 5:
        return 100
    elif 5 < dev < 300:
        return 101.133663 * (0.9979 ** dev)
    return -100


def get_judgements(deviations: list) -> dict:
    """Calculate judgements based on a list of hit deviations.
    :param deviations: Hit deviations
    :return: dict with numbers of perfects, decents, goods, mehs, and misses in order"""
    perfects = 0
    decents = 0
    goods = 0
    mehs = 0
    misses = 0
    for dev in deviations:
        dev = abs(dev)
        if dev < 20:
            perfects += 1
        elif dev < 50:
            decents += 1
        elif dev < 100:
            goods += 1
        elif dev < 300:
            mehs += 1
        else:
            misses += 1
    return {"perfects": perfects, "decents": decents, "goods": goods, "mehs": mehs, "misses": misses}


def get_single_dev_judgement(dev: float):
    """Given a single deviation, returns an int from
    0-4 where 0 is a perfect and 4 is a miss"""
    a_dev = abs(dev)
    if a_dev < 20:
        return 0
    elif a_dev < 50:
        return 1
    elif a_dev < 100:
        return 2
    elif a_dev < 300:
        return 3
    return 4


def check_mouse_clicked(events: list[pygame.event.Event]):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return True
    return False
