import pygame
from constants import *
import utils
import tween
import math
import time
import json
import backgrounds.cdbounce
from tween import *
from text import Text
from results import Results, save_score, judgement_colors
from enums import ScreenEnum

judgement_names = ("perfect!", "decent", "good", "meh", "miss")


class LiveAccuracy:
    def __init__(self):
        self.accuracy_sum = 0
        self.notes_passed = 0
        self.curr_accuracy = 0.0
        self.text = Text("00.00%", (20, 20), (255, 255, 255))

    def update(self, hit_dev: float):
        self.accuracy_sum += utils.single_deviation_acc(hit_dev)
        self.notes_passed += 1
        self.curr_accuracy = round((self.accuracy_sum / self.notes_passed), 2)
        self.text.change_text(str(self.curr_accuracy) + "%")

    def render(self):
        self.text.blit(SCREEN)


# the grid class also includes the player
class Note:
    def __init__(self, note_time: float, square_n: int, visible_duration: float):
        """
        Note in a chart
        :param note_time: Where the note is in seconds
        :param square_n: The number of the square the note is in from 1-25
         (ex. row 2 column 4 has a square number of 9)
        """
        self.note_time = note_time
        self.visible = False
        self.scale = 0
        self.scale_tween = None
        self.in_late_window = False
        self.hit = False
        self.was_not_hit = False
        # default value of 3000ms so hit_deviation is calculated as a miss
        # in case it doesn't get caught as a miss in the hit detection
        self.hit_deviation = 3000  # in milliseconds
        self.visible_duration = visible_duration  # in seconds
        self.surface = None
        self.color = (200, 200, 240)
        # square_n = (row - 1) * 5 + column
        # square_n = 5(y - 1) + x
        self.square_n = square_n
        self.x = square_n % 5
        self.y = square_n // 5

    def render(self, chart_time: float, is_hit: bool, grid_x, grid_y, time_offset: float = 0):
        if chart_time >= self.note_time - self.visible_duration \
                and not self.visible and not self.was_not_hit and not self.hit:
            self.visible = True
            self.scale_tween = Tween(EaseLinear, 1, 75, self.visible_duration)
            self.surface = pygame.Surface((75, 75))
            self.surface.fill(self.color)

        if self.visible:
            self.scale_tween.update(time_offset)
            self.scale = int(self.scale_tween.curr_val)
            self.surface = pygame.transform.scale(self.surface, (self.scale, self.scale))
            if is_hit:
                self.hit = True
                self.hit_deviation = 1000 * (chart_time - self.note_time)
                self.visible = False
                # add cool animation later

            if chart_time > self.note_time:
                if not self.scale_tween.end_val == 1:
                    self.scale_tween = Tween(EaseLinear, 75, 1, self.visible_duration)
                else:
                    if self.scale_tween.done and self.scale_tween.end_val == 1 and not self.hit:
                        self.was_not_hit = True
                        self.hit_deviation = 3000
                        self.visible = False
        if self.visible:
            SCREEN.blit(self.surface, pygame.Rect(grid_x + self.x * 80 + 5, grid_y + self.y * 80 + 5, 74, 74))
        ...


class Grid:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/grid.png")
        self.square_image = pygame.image.load("assets/square.png")
        self.x = x
        self.y = y

        self.square_x = 0
        self.square_y = 0

        self.square_n = 0

        self.square_actual_x = self.x + 5
        self.square_actual_y = self.y + 5

        self.x_tween = tween.Tween(tween.EaseLinear, self.square_actual_x, self.square_actual_x, 0)
        self.y_tween = tween.Tween(tween.EaseLinear, self.square_actual_y, self.square_actual_y, 0)

    def move_square(self, x, y):
        if 0 <= self.square_x + x <= 4:
            self.square_x += x
            self.square_n += x
            self.x_tween = tween.Tween(tween.EaseSineInOut, (self.square_x - x) * 80 + self.x + 5,
                                       self.square_x * 80 + self.x + 5, 0.08)

        if 0 <= self.square_y + y <= 4:
            self.square_y += y
            self.square_n += y * 5
            self.y_tween = tween.Tween(tween.EaseSineInOut, (self.square_y - y) * 80 + self.y + 5,
                                       self.square_y * 80 + self.y + 5, 0.08)

    def blit(self):
        if self.x_tween:
            self.x_tween.update()
            self.square_actual_x = self.x_tween.curr_val
        if self.y_tween:
            self.y_tween.update()
            self.square_actual_y = self.y_tween.curr_val

        SCREEN.blit(self.square_image, (self.square_actual_x, self.square_actual_y))
        SCREEN.blit(self.image, (self.x, self.y))

    def reset_grid(self):
        self.square_n = 0
        self.square_x = 0
        self.square_y = 0
        self.square_actual_x = self.x + 5
        self.square_actual_y = self.y + 5
        self.x_tween = None
        self.y_tween = None


grid = Grid(SIZE[0] // 2 - 405 // 2, SIZE[1] - 500)


class Chart:
    def __init__(self, notes: list[Note], song_name: str, song_artist: str,
                 song_filename: str, song_start: float):
        self.combo = 0
        self.image = pygame.image.load("assets/note.png")
        self.notes = notes
        self.song_start = song_start
        pygame.mixer.music.load(song_filename)
        self.length = pygame.mixer.Sound(song_filename).get_length()
        self.info = f"{song_artist} - {song_name}"

        self.chart_clock = time.time()
        self.hit_deviations = []
        self.curr_acc = LiveAccuracy()

        self.progress_bar_width = SIZE[0] // 2
        self.progress_bar_x = SIZE[0] // 5

        self.hp_x_pos = SIZE[0] - 80
        self.hp_y_pos = SIZE[1] - 500
        self.hp_width = 50
        self.hp_height = 400
        self.hp_curr_height = self.hp_height

        self.hp_color = (255, 50, 50)
        self.hp_bg_color = (120, 100, 120)

        self.started = False
        self.finished = False
        self.paused = False

        self.pause_time = 0
        self.pause_total_time = 0

        self.progress_rect_bg = pygame.Rect(self.progress_bar_x, 20, self.progress_bar_width, 50)
        self.progress_rect_fg = pygame.Rect(self.progress_bar_x, 20, 1, 50)

        self.hp = 100
        self.hp_rect = pygame.Rect(self.hp_x_pos, self.hp_y_pos, self.hp_width, self.hp_height)
        self.hp_bg_rect = self.hp_rect

        self.text = Text(self.info, (SIZE[0] // 5, 40), font=BASE_FONT)
        self.judgement_texts: list[Text] = [Text(t, (1000, 240), judgement_colors[num]) for num, t in enumerate(judgement_names)]
        self.combo_text = Text("combo 0", (1000, 200))
        self.combo_changed = False

        self.current_judge = None
    def start(self):
        self.chart_clock = time.time()
        from options import MUSIC_VOLUME, SFX_VOLUME
        pygame.mixer.music.set_volume(MUSIC_VOLUME / 100)
        SOUND_NOTE_HIT.set_volume(SFX_VOLUME / 100)
        pygame.mixer.music.play()
        self.started = True
        ...

    def render_notes(self, curr_grid: Grid, hit_note: bool):
        if self.paused:
            self.paused = False
            self.pause_total_time += time.time() - self.pause_time
            pygame.mixer.music.play(start=time.time() - self.chart_clock - self.pause_total_time)

            self.pause_time = 0

        time_diff = time.time() - self.chart_clock - self.pause_total_time
        if time_diff > 0:
            for note in self.notes[:10]:
                if curr_grid.square_n == note.square_n and hit_note:
                    SOUND_NOTE_HIT.stop()
                    SOUND_NOTE_HIT.play()
                    note.render(time_diff, True, curr_grid.x, curr_grid.y)
                    self.hit_deviations.append(note.hit_deviation)
                    if note.hit_deviation < 100:
                        self.hp += 5
                    else:
                        self.hp += 2
                    self.combo += 1
                    self.combo_changed = True
                    self.current_judge = utils.get_single_dev_judgement(note.hit_deviation)
                    self.curr_acc.update(note.hit_deviation)
                    self.notes.pop(0)

                else:
                    note.render(time_diff, False, curr_grid.x, curr_grid.y)
                    if note.was_not_hit:
                        self.hp -= 12
                        self.hit_deviations.append(note.hit_deviation)
                        self.curr_acc.update(note.hit_deviation)
                        self.current_judge = 4
                        self.combo = 0
                        self.combo_changed = True
                        self.notes.pop(0)

        if self.hp <= 0:
            self.finished = True
            self.curr_acc.curr_accuracy = -100
        else:
            self.hp = utils.clamp(self.hp, 0, 100)

    def render_ui(self):
        # render progress bar
        time_elapsed = time.time() - self.chart_clock - self.pause_total_time
        curr_progress = utils.clamp(time_elapsed / self.length, 0, 1)
        self.progress_rect_fg = pygame.Rect(self.progress_bar_x, 20, int(curr_progress * self.progress_bar_width), 50)
        pygame.draw.rect(SCREEN, (100, 100, 100), self.progress_rect_bg)
        pygame.draw.rect(SCREEN, (60, 60, 90), self.progress_rect_fg)
        self.text.blit(SCREEN)
        if time_elapsed >= self.length:
            self.finished = True

        # render live accuracy
        self.curr_acc.render()

        # render HP bar
        self.hp_curr_height = self.hp_height * (self.hp / 100)
        self.hp_rect = pygame.Rect(self.hp_x_pos, self.hp_y_pos - self.hp_curr_height + self.hp_height, self.hp_width,
                                   self.hp_curr_height)
        pygame.draw.rect(SCREEN, self.hp_bg_color, self.hp_bg_rect)
        pygame.draw.rect(SCREEN, self.hp_color, self.hp_rect)

        # render combo and current judgement text
        if self.combo_changed:
            self.combo_changed = False
            self.combo_text.change_text(f"{self.combo} combo")
        self.combo_text.blit(SCREEN)
        if self.current_judge is not None:
            self.judgement_texts[self.current_judge].blit(SCREEN)


    def pause(self):
        self.paused = True
        pygame.mixer.music.pause()
        self.pause_time = time.time()


def load_chart(chart_filename: str) -> Chart:
    # after metadata JSON first line, chart files contain only notes.
    # each line after contains info of a note, and is formatted as:
    # [square_n] [note_time]
    f = open(chart_filename, "r")
    notes_list = []
    song_name = song_artist = None
    song_offset = None
    visible_difficulty = None
    song_filename = None
    for line in f.readlines():
        if "{" not in line:
            square_n, note_time = line.split()
            square_n = int(square_n)
            note_time = float(note_time)
            notes_list.append(Note(note_time, square_n, visible_difficulty))
        else:
            metadata = json.loads(line)
            song_name = metadata['song_name']
            song_artist = metadata['artist']
            song_filename = metadata['song_file']
            song_offset = metadata['song_offset']
            visible_difficulty = metadata['visible_difficulty']

    f.close()

    return Chart(notes_list, song_name, song_artist, song_filename, song_offset)


chart_locations = ["assets/chart1test.cf", None, None, None]
# leave None as a placeholder if the chart is not implemented yet
chart_list = [load_chart(chart_loc) for chart_loc in chart_locations if chart_loc]
gameplay_chart_list = chart_list


def gameplay_screen(events, chart_n: int):
    if not gameplay_chart_list[chart_n].started:
        gameplay_chart_list[chart_n].start()
    elif gameplay_chart_list[chart_n].finished:
        finished_chart = gameplay_chart_list[chart_n]

        # Bug fix. this prevents a bug causing the player to immediately be
        # redirected to the results/score screen when they want to play the
        # chart again. loading a completely new chart from the
        # chart location instead of just leaving it there solves the issue
        gameplay_chart_list[chart_n] = load_chart(chart_locations[chart_n])

        grid.reset_grid()
        return Results(finished_chart.hit_deviations, finished_chart.curr_acc.curr_accuracy,
                       finished_chart.text)

    SCREEN.fill((0, 0, 0))
    backgrounds.cdbounce.render_rects(SCREEN)
    hit_note = False

    keys_pressed = pygame.key.get_pressed()
    movement_mult = 1
    if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
        movement_mult = 2
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.dict['key'] == pygame.K_UP:
                grid.move_square(0, -1 * movement_mult)
            if event.dict['key'] == pygame.K_DOWN:
                grid.move_square(0, 1 * movement_mult)
            if event.dict['key'] == pygame.K_LEFT:
                grid.move_square(-1 * movement_mult, 0)
            if event.dict['key'] == pygame.K_RIGHT:
                grid.move_square(1 * movement_mult, 0)
            if event.dict['key'] == pygame.K_SPACE:
                hit_note = True
            if event.dict['key'] == pygame.K_ESCAPE:
                gameplay_chart_list[chart_n].pause()
                return ScreenEnum.PAUSE

    grid.blit()
    gameplay_chart_list[chart_n].render_notes(grid, hit_note)
    gameplay_chart_list[chart_n].render_ui()
    pygame.display.update()
