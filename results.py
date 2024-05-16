import pygame
from utils import single_deviation_acc, get_judgements
from text import Text, TextOptionMenu
from constants import *

judgement_colors = [(50, 255, 50), (255, 255, 20), (90, 30, 100), (100, 90, 30), (255, 10, 10)]

class Results:
    def __init__(self, hit_deviations: list[float], accuracy: float, chart_info_text: Text):
        self.hit_devs = hit_deviations
        self.accuracy = accuracy
        self.judgements = get_judgements(self.hit_devs)
        self.text_acc = Text(str(self.accuracy) + "%", (SIZE[0] - 100, SIZE[1] // 2))
        self.text_chart_info = chart_info_text

        if self.accuracy < 65:
            self.failed = True
        else:
            self.failed = False
        self.judgement_texts = [Text(
            judgement_text,
            (100, SIZE[1] // 4 + num * 30),
            judgement_colors[num])
            for num, judgement_text in enumerate(f"{key}: {self.judgements[key]}" for key in self.judgements)]

    def render(self):
        for text in self.judgement_texts:
            text.blit(screen)
        self.text_acc.blit(screen)
        self.text_chart_info.blit(screen)


exit_menu = TextOptionMenu(BASE_FONT, (200, 200, 250), (255, 50, 50), (20, 20), ["exit"])
def results_screen(events, chart_results: Results):
    screen.fill((0, 0, 0))
    # render text & options next
    mouse_clicked = False
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True
    mouse_pos = pygame.mouse.get_pos()
    chart_results.render()
    hovered_opt, clicked_opt = exit_menu.get_interacted(mouse_pos, mouse_clicked)
    if clicked_opt:
        return 1
    exit_menu.blit(screen)
    pygame.display.update()
