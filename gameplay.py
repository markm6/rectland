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
from results import Results, save_score


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
        self.text.blit(screen)


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
        self.y = math.floor((square_n - 1) / 5) if square_n > 0 else 0

    def render(self, chart_time: float, is_hit: bool, grid_x, grid_y):
        if chart_time >= self.note_time - self.visible_duration \
                and not self.visible and not self.was_not_hit and not self.hit:
            self.visible = True
            self.scale_tween = Tween(EaseLinear, 1, 75, self.visible_duration)
            self.surface = pygame.Surface((75, 75))
            self.surface.fill(self.color)

        if self.visible:
            self.scale_tween.update()
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
            screen.blit(self.surface, pygame.Rect(grid_x + self.x * 80 + 5, grid_y + self.y * 80 + 5, 74, 74))
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
        if (self.square_x < 4 and x > 0) or (self.square_x > 0 > x):
            self.square_x += x
            self.square_n += x
            self.x_tween = tween.Tween(tween.EaseSineInOut, (self.square_x - x) * 80 + self.x + 5,
                                       self.square_x * 80 + self.x + 5, 0.08)
        if (self.square_y < 4 and y > 0) or (self.square_y > 0 > y):
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

        screen.blit(self.square_image, (self.square_actual_x, self.square_actual_y))
        screen.blit(self.image, (self.x, self.y))

    def reset_grid(self):
        self.square_n = 0
        self.square_x = 0
        self.square_y = 0
        self.square_actual_x = self.x + 5
        self.square_actual_y = self.y + 5
        self.x_tween = None
        self.y_tween = None


grid = Grid(SIZE[0] // 2 - 405, SIZE[1] - 500)


# wondering on how I should have chart class interact with grid in code... will think about this at home
class Chart:
    def __init__(self, notes: list[Note], song_name: str, song_artist: str,
                 song_filename: str, song_start: float):

        self.image = pygame.image.load("assets/note.png")
        self.notes = notes
        self.song_start = song_start
        self.song_file = pygame.mixer.Sound(song_filename)
        self.length = self.song_file.get_length()
        self.info = f"{song_artist} - {song_name}"

        self.chart_clock = time.time()
        self.hit_deviations = []
        self.curr_acc = LiveAccuracy()
        self.progress_bar_width = SIZE[0] // 2
        self.progress_bar_x = SIZE[0] // 5
        self.started = False
        self.finished = False

        self.progress_rect_bg = pygame.Rect(self.progress_bar_x, 20, self.progress_bar_width, 50)
        self.progress_rect_fg = pygame.Rect(self.progress_bar_x, 20, 1, 50)
        self.text = Text(self.info, (SIZE[0] // 5, 52), font=INFO_FONT)

    def start(self):
        self.chart_clock = time.time()
        self.song_file.play()
        self.started = True
        ...

    def render_notes(self, curr_grid: Grid, hit_note: bool):
        time_diff = time.time() - self.chart_clock
        if time_diff > 0:
            for note in self.notes[:10]:
                if curr_grid.square_n == note.square_n and hit_note:
                    note.render(time_diff, True, curr_grid.x, curr_grid.y)
                    self.hit_deviations.append(note.hit_deviation)
                    self.curr_acc.update(note.hit_deviation)
                    self.notes.pop(0)

                else:
                    note.render(time_diff, False, curr_grid.x, curr_grid.y)
                    if note.was_not_hit:
                        self.hit_deviations.append(note.hit_deviation)
                        self.curr_acc.update(note.hit_deviation)
                        self.notes.pop(0)

    def render_progress(self):
        time_elapsed = time.time() - self.chart_clock
        curr_progress = utils.clamp(time_elapsed / self.length, 0, 1)
        self.progress_rect_fg = pygame.Rect(self.progress_bar_x, 20, int(curr_progress * self.progress_bar_width), 50)
        pygame.draw.rect(screen, (100, 100, 100), self.progress_rect_bg)
        pygame.draw.rect(screen, (60, 60, 90), self.progress_rect_fg)
        # TODO: refactor everything to not require scr param
        self.text.blit(screen)
        if time_elapsed >= self.length:
            self.finished = True

    def render_live_acc(self):
        self.curr_acc.render()


def load_chart(chart_filename: str) -> Chart:
    # before metadata, chart files contain only notes.
    # each line after contains info of a note, and is formatted as:
    # [square_n] [note_time]
    # then, metadata is loaded at end of file for convenience of coding this
    # should change this later though! metadata should probably come first
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

    screen.fill((0, 0, 0))
    backgrounds.cdbounce.render_rects(screen)
    gameplay_chart_list[chart_n].render_progress()
    hit_note = False
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.dict['key'] == pygame.K_UP:
                grid.move_square(0, -1)
            if event.dict['key'] == pygame.K_DOWN:
                grid.move_square(0, 1)
            if event.dict['key'] == pygame.K_LEFT:
                grid.move_square(-1, 0)
            if event.dict['key'] == pygame.K_RIGHT:
                grid.move_square(1, 0)
            if event.dict['key'] == pygame.K_SPACE:
                hit_note = True

    grid.blit()
    gameplay_chart_list[chart_n].render_notes(grid, hit_note)
    gameplay_chart_list[chart_n].render_live_acc()
    pygame.display.update()
