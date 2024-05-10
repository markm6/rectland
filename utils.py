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
        elif 5 < dev < 878:
            converted_accuracies.append(100 - 0.001*((dev - 5)**1.7))
        if dev > 2500:
            converted_accuracies.append(-100)
    return sum(converted_accuracies) / len(converted_accuracies)