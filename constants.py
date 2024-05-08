import pygame
import os
pygame.init()
pygame.font.init()
pygame.display.init()

os.environ["SDL_VIDEO_CENTERED"] = "1"

SIZE = (1280, 720)
BASE_FONT = pygame.font.SysFont('Arial', 30)
INFO_FONT = pygame.font.SysFont('Arial', 15)
CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)