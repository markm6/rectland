import pygame
from utils import single_deviation_acc, get_judgements
from text import Text, TextOptionMenu
from constants import *
import json
import uuid
import datetime
import math
from utils import check_mouse_clicked

judgement_colors = ((50, 255, 50), (255, 255, 20), (90, 30, 100), (100, 90, 30), (255, 10, 10))
failed_text = Text("failed", (SIZE[0] - 200, 20), (255, 10, 10))


class Results:
    def __init__(self, hit_deviations: list[float], accuracy: float, chart_info_text: Text):
        self.hit_devs = hit_deviations
        self.accuracy = accuracy
        self.judgements = get_judgements(self.hit_devs)
        self.text_acc = Text(str(self.accuracy) + "%", (100, 100), font=SEMI_BIG_FONT)
        self.text_chart_info = chart_info_text
        self.text_chart_info.change_font(BASE_FONT)
        self.date_time = datetime.datetime.now()
        self.mean = round(sum(self.hit_devs) / len(self.hit_devs), 2)
        self.mean_devs = [(dev - self.mean) ** 2 for dev in self.hit_devs]
        self.std_dev = round(math.sqrt(sum(self.mean_devs) / (len(self.hit_devs))), 2)
        # TODO: make texts and render them (finish at home)

        if self.accuracy < 65:
            self.failed = True
        else:
            self.failed = False
        self.judgement_texts = [Text(
            judgement_text,
            (100, SIZE[1] // 4 + num * 30),
            judgement_colors[num])
            for num, judgement_text in enumerate(f"{key}: {self.judgements[key]}" for key in self.judgements)]
        self.mean_text = Text(f"mean: {self.mean}ms", (100, 400))
        self.std_dev_text = Text(f"std. dev: {self.std_dev}ms", (100, 450))

    def render(self):
        for text in self.judgement_texts:
            text.blit(SCREEN)
        if self.failed:
            failed_text.blit(SCREEN)
        self.text_acc.blit(SCREEN)
        self.text_chart_info.blit(SCREEN)
        self.mean_text.blit(SCREEN)
        self.std_dev_text.blit(SCREEN)

    def to_json(self):
        return {"chart_name": self.text_chart_info.display_text,
                "hit_devs": self.hit_devs, "accuracy": self.accuracy,
                "judgements": self.judgements, "date": str(self.date_time),
                "failed": self.failed}


exit_menu = TextOptionMenu(BASE_FONT, (200, 200, 250), (255, 50, 50), (20, 20), ["exit"])


def save_score(chart_res: Results):
    uid = uuid.uuid4().hex
    f = open("scores/scores.json", "r")
    data = f.read()
    f.close()

    chart_song_inf = chart_res.text_chart_info.display_text
    if len(data) > 1:
        scores_json: dict = json.loads(data)
        # structure:
        # {song_inf: {'0a473894': results} }
        if chart_song_inf in scores_json.keys():
            scores_json[chart_song_inf].update({uid: chart_res.to_json()})
    else:
        scores_json = {chart_song_inf: {uid: chart_res.to_json()}}

    f = open("scores/scores.json", "w")
    # https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
    json.dump(scores_json, f)
    f.close()


def results_screen(events, chart_results: Results):
    SCREEN.fill((0, 0, 0))
    # render text & options next
    mouse_clicked = check_mouse_clicked(events)
    mouse_pos = pygame.mouse.get_pos()
    chart_results.render()
    hovered_opt, clicked_opt = exit_menu.get_interacted(mouse_pos, mouse_clicked)
    if clicked_opt == 0:
        save_score(chart_results)
        return 1
    exit_menu.blit(SCREEN)
    pygame.display.update()
