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
