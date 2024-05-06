import pygame
from constants import *
import utils
import tween
import math
import time

# the grid class also includes the player
class Note:
    def __init__(self, note_time: float, square_n: int):
        """
        Note in a chart
        :param note_time: Where the note is in seconds
        :param square_n: The number of the square the note is in from 1-25
         (ex. row 2 column 4 has a square number of 9)
        """
        self.note_time = note_time
        self.active = False
        # square_n = (row - 1) * 5 + column
        # square_n = 5(y - 1) + x
        self.square_n = square_n
        self.x = square_n % 5
        self.y = math.floor((square_n - 1) / 5) if square_n > 0 else 0

# wondering on how I should have chart class interact with grid in code... will think about this at home
class Chart:
    def __init__(self, notes: list[Note], song_filename: str, song_start: float):
        self.image = pygame.image.load("note.png")
        self.notes = notes
        self.song_start = song_start
        self.song_filename = song_filename
        self.chart_clock = time.time() - 2 # allow 2 seconds of time for intro
    def start(self):
        pygame.mixer_music.load(self.song_filename)
        pygame.mixer_music.play(0, self.song_start)
        self.chart_clock = time.time() - 2
    def update(self):
        for note in self.notes:
            if note.note_time - self.chart_clock < 0.5:
                note.active = True


class Grid:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/grid.png")
        self.square_image = pygame.image.load("assets/square.png")

        self.x = x
        self.y = y

        self.square_x = 0
        self.square_y = 0

        self.square_actual_x = self.x + 5
        self.square_actual_y = self.y + 5

        self.x_tween = tween.Tween(tween.EaseLinear, self.square_actual_x, self.square_actual_x, 0)
        self.y_tween = tween.Tween(tween.EaseLinear, self.square_actual_y, self.square_actual_y, 0)


    def move_square(self, x, y):
        if (self.square_x < 4 and x > 0) or (self.square_x > 0 > x):
            self.square_x += x
            self.x_tween = tween.Tween(tween.EaseSineInOut, (self.square_x - x) * 80 + self.x + 5,
                                       self.square_x * 80 + self.x + 5, 0.08)
        if (self.square_y < 4 and y > 0) or (self.square_y > 0 > y):
            self.square_y += y
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





grid = Grid(SIZE[0] // 2 - 405, SIZE[1] - 500)


def gameplay_screen(events):
    CLOCK.tick(60)
    screen.fill((0, 0, 0))

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

    grid.blit()
    pygame.display.update()
