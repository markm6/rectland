import pygame
from constants import *

pygame.font.init()


class Text:
    def __init__(self, display_text: str, position: tuple[int, int], color=(255, 255, 255), font=BASE_FONT):
        self.font = font
        self.color = color
        self.display_text = display_text
        self.text_obj = font.render(display_text, True, color)
        self.x, self.y = position
        self.rect = pygame.Rect(self.x, self.y, self.text_obj.get_width(), self.text_obj.get_height())

    def change_text(self, new_display_text: str):
        self.display_text = new_display_text
        self.text_obj = self.font.render(new_display_text, True, self.color)
        self.rect = pygame.Rect(self.x, self.y, self.text_obj.get_width(), self.text_obj.get_height())

    def change_font(self, new_font: pygame.font.Font):
        self.font = new_font
        self.text_obj = self.font.render(self.display_text, True, self.color)
        self.rect = pygame.Rect(self.x, self.y, self.text_obj.get_width(), self.text_obj.get_height())

    def change_color(self, new_color: tuple[int, int, int]):
        self.color = new_color
        self.text_obj = self.font.render(self.display_text, True, new_color)

    def blit(self, scr: pygame.Surface):
        scr.blit(self.text_obj, (self.x, self.y))


class TextOptionMenu:
    def __init__(self, font: pygame.font.Font, color, selected_color: tuple[int, int, int],
                 start_pos: tuple[int, int], options: list[str]):
        self.selected_color = selected_color
        self.default_color = color
        self.font_height = font.get_height()

        self.text_options = [Text(
            opt,
            (start_pos[0], start_pos[1] + num * (self.font_height + 10)),
            color, font)
            for num, opt in enumerate(options)]

    def get_interacted(self, mouse_pos: tuple[int, int], clicked: bool = False):
        hovered_opt = None
        clicked_opt = None
        for i in range(len(self.text_options)):
            if self.text_options[i].rect.collidepoint(mouse_pos):
                self.text_options[i].change_color(self.selected_color)
                hovered_opt = i
                if clicked:
                    clicked_opt = i
            elif self.text_options[i].color == self.selected_color:
                self.text_options[i].change_color(self.default_color)

        return hovered_opt, clicked_opt

    def blit(self, scr: pygame.Surface):
        for text in self.text_options:
            text.blit(scr)
