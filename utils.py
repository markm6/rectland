import pygame

def check_quit(events):
    return pygame.event.Event(256) in events

def quit_game():
    pygame.quit()
    exit(0)
