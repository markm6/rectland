import pygame
from constants import *
import utils
import tween
import math
import time
import json
from tween import Tween, EaseLinear
from text import Text


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
        self.hit_deviation = None  # in milliseconds
        self.visible_duration = visible_duration  # in seconds
        self.surface = None

        # square_n = (row - 1) * 5 + column
        # square_n = 5(y - 1) + x
        self.square_n = square_n
        self.x = square_n % 5
        self.y = math.floor((square_n - 1) / 5) if square_n > 0 else 0

    def render(self, screen: pygame.Surface, chart_time: float, is_hit: bool, grid_x, grid_y):
        if chart_time >= self.note_time - self.visible_duration \
                and not self.visible and not self.was_not_hit:
            self.visible = True
            self.scale_tween = Tween(EaseLinear, 0, 78, self.visible_duration)
            self.surface = pygame.Surface((75, 75))
            self.surface.fill((30, 255, 10))


        if self.visible:
            self.scale_tween.update()

            self.scale = int(self.scale_tween.curr_val) + 1
            self.surface = pygame.transform.scale(self.surface, (self.scale, self.scale))
            if is_hit:
                self.hit = True
                self.hit_deviation = 1000 * (chart_time - self.note_time)
            if chart_time > self.note_time:
                if not self.scale_tween:
                    self.scale_tween = Tween(EaseLinear, 78, 0, self.visible_duration)
                else:
                    if self.scale_tween.done and not self.hit:
                        self.was_not_hit = True
                        self.hit_deviation = 3000
                        self.visible = False
        if self.visible:
            print(f"{self} blitted")
            screen.blit(self.surface, pygame.Rect(grid_x + self.x * 80, grid_y + self.y * 80, 75, 75))
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
        print(self.square_n)

    def blit(self):
        if self.x_tween:
            self.x_tween.update()
            self.square_actual_x = self.x_tween.curr_val
        if self.y_tween:
            self.y_tween.update()
            self.square_actual_y = self.y_tween.curr_val

        screen.blit(self.square_image, (self.square_actual_x, self.square_actual_y))
        screen.blit(self.image, (self.x, self.y))


grid = Grid(SIZE[0] // 2 - 405, SIZE[1] - 500)


# wondering on how I should have chart class interact with grid in code... will think about this at home
class Chart:
    def __init__(self, notes: list[Note], song_name: str, song_artist: str,
                 song_filename: str, song_start: float, grid: Grid):
        self.image = pygame.image.load("assets/note.png")
        self.notes = notes
        self.song_start = song_start
        self.song_file = pygame.mixer.Sound(song_filename)
        self.length = self.song_file.get_length()
        self.info = f"{song_artist} - {song_name}"
        self.chart_clock = time.time() + 2  # allow 2 seconds of time for intro

        self.progress_bar_width = SIZE[0] // 3

        self.progress_rect_bg = pygame.Rect(SIZE[0] // 3, 20, SIZE[0] // 2, 50)
        self.progress_rect_fg = pygame.Rect(SIZE[0] // 3, 20, 1, 50)
        self.text = Text(self.info, (SIZE[0] // 3, 52), font=INFO_FONT)

    def start(self):
        self.chart_clock = time.time() + 2
        # handle audio later, need to figure out
        # if audio object should be used
        # or just mixer module (probably mixer for now)
        ...

    def render_notes(self, curr_grid: Grid, hit_note: bool):
        time_diff = time.time() - self.chart_clock
        if time_diff > 0:
            for note in self.notes[:10]:
                if curr_grid.square_n == note.square_n and hit_note:
                    note.render(screen, time_diff, True, curr_grid.x, curr_grid.y)
                else:
                    note.render(screen, time_diff, False, curr_grid.x, curr_grid.y)

    def render_progress(self):
        curr_progress = utils.clamp((time.time() - self.chart_clock) / self.length, 0, 1)
        self.progress_rect_fg = pygame.Rect(SIZE[0] // 3, 20, int(curr_progress * self.progress_bar_width), 50)
        pygame.draw.rect(screen, (100, 100, 100), self.progress_rect_bg)
        pygame.draw.rect(screen, (255, 255, 0), self.progress_rect_fg)
        # TODO: refactor everything to not require scr param
        self.text.blit(screen)


def load_chart(chart_filename: str, song_filename: str, grid: Grid) -> Chart:
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
    for line in f.readlines():
        if "{" not in line:
            square_n, note_time = map(int, line.split())
            notes_list.append(Note(note_time, square_n, visible_difficulty))
        else:
            metadata = json.loads(line)
            song_name = metadata['song_name']
            song_artist = metadata['artist']
            song_offset = metadata['song_offset']
            visible_difficulty = metadata['visible_difficulty']
    f.close()

    return Chart(notes_list, song_name, song_artist, song_filename, song_offset, grid)


test_chart = load_chart("assets/chart1test.cf", "assets/file_example_MP3_1MG.mp3", grid)


def gameplay_screen(events):
    CLOCK.tick(60)
    screen.fill((0, 0, 0))
    test_chart.render_progress()
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

    test_chart.render_notes(grid, True)
    grid.blit()
    pygame.display.update()
