import pygame
from constants import *
from slider import Slider
from text import Text
from utils import check_mouse_clicked

SFX_VOLUME = 50
MUSIC_VOLUME = 50

menu_text = Text("options", (50, 100), font=BIG_FONT)
sfx_text = Text("sfx volume:", (50, 200))
music_text = Text("music volume:", (50, 300))
sfx_slider = Slider(50, 250, True, 0, 100)
music_slider = Slider(50, 350, True, 0, 100)

def options_menu(events):
    global SFX_VOLUME, MUSIC_VOLUME
    mouse_pos = pygame.mouse.get_pos()
    buttons_pressed = pygame.mouse.get_pressed(3)
    print(buttons_pressed)
    screen.fill((0, 0, 0))
    menu_text.blit(screen)
    sfx_text.blit(screen)
    music_text.blit(screen)
    music_slider.render(mouse_pos[0], mouse_pos[1], buttons_pressed[0])
    sfx_slider.render(mouse_pos[0], mouse_pos[1], buttons_pressed[0])
    if buttons_pressed[0]:
        SFX_VOLUME = sfx_slider.curr_val
        MUSIC_VOLUME = music_slider.curr_val

    pygame.display.flip()

