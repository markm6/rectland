import pygame
from constants import *
from text import Text

class Slider:
    def __init__(self, x, y, is_percent: bool, min_val, max_val):
        self.slider_img = pygame.image.load("assets/slider.png")
        self.slider_knob_img = pygame.image.load("assets/slider knob.png")
        self.x = x
        self.y = y
        self.knob_x = self.x + 5
        self.knob_y = self.y + 5
        self.is_percent = is_percent
        self.min_val = min_val
        self.curr_val = min_val
        self.max_val = max_val
        self.val_text = Text(str(min_val) + "%" if self.is_percent else str(min_val),
                             (self.x + 260, self.y))

    def render(self, mouse_x, mouse_y, mouse_down: bool):
        if mouse_down and self.x + 5 <= mouse_x <= self.x + 245 and self.knob_y <= mouse_y <= self.knob_y + 40:
            self.knob_x = mouse_x
            self.curr_val = self.min_val + (self.max_val - self.min_val) \
                            * ((self.knob_x - self.x) / 245)
            self.val_text.change_text(f"{round(self.curr_val)}{'%' if self.is_percent else ''}")
        screen.blit(self.slider_img, (self.x, self.y))
        screen.blit(self.slider_knob_img, (self.knob_x, self.knob_y))
        self.val_text.blit(screen)