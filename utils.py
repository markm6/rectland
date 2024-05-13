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

def accuracy_calc(deviations: list):
    converted_accuracies = []
    for dev in deviations:
        dev = abs(dev)
        if dev < 5:
            converted_accuracies.append(100)
        elif 5 < dev < 400:
            converted_accuracies.append(100 - 0.001*((dev - 5)**1.925))
        else:
            converted_accuracies.append(-100)
    return sum(converted_accuracies) / len(converted_accuracies)


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
        if dev < 10:
            perfects += 1
        elif dev < 25:
            decents += 1
        elif dev < 100:
            goods += 1
        elif dev < 400:
            mehs += 1
        else:
            misses += 1
    return {"perfects": perfects, "decents": decents, "goods": goods, "mehs": mehs, "misses": misses}