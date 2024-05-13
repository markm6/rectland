import pygame
from gameplay import Chart
from utils import accuracy_calc, get_judgements
from text import Text
from constants import *

class Results:
    def __init__(self, chart: Chart):
        self.chart = chart
        self.hit_devs = self.chart.hit_deviations
        self.accuracy = accuracy_calc(self.hit_devs)
        self.judgements = get_judgements(self.hit_devs)
        self.text_acc = Text(str(self.accuracy) + "%", (SIZE[0] - 100, SIZE[1] // 2))
        self.text_chart_info = self.chart.text

        if self.accuracy < 65:
            self.failed = True
        else:
            self.failed = False
        self.judgement_texts = [Text(
            judgement_text,
            (100, SIZE[1] // 4 + num * 30),
            [(50, 255, 50), (255, 255, 20), (90, 30, 100), (100, 90, 30), (255, 10, 10)][num])
            for num, judgement_text in enumerate(f"{key}: {self.judgements[key]}" for key in self.judgements)]

    def render(self):
        for text in self.judgements:
            text.blit(screen)
        self.text_acc.blit(screen)
        self.text_chart_info.blit(screen)
