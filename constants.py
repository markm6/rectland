import pygame
import os
pygame.init()
pygame.font.init()
pygame.display.init()

os.environ["SDL_VIDEO_CENTERED"] = "1"

SIZE = (1280, 720)
SOUND_NOTE_HIT = pygame.mixer.Sound("assets/sound note tick.wav")
BASE_FONT = pygame.font.SysFont('Arial', 30)
SEMI_BIG_FONT = pygame.font.SysFont('Arial', 45)
BIG_FONT = pygame.font.SysFont('Arial', 60)
INFO_FONT = pygame.font.SysFont('Arial', 15)
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode(SIZE)
