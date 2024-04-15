import pygame
from constants import *
import utils
import tween


# the grid class also includes the player
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
        if (self.square_x < 4 and x > 0) or (self.square_x > 0 and x < 0):
            self.square_x += x
            self.x_tween = tween.Tween(tween.EaseSineInOut, (self.square_x - x) * 80 + self.x + 5,
                                           self.square_x * 80 + self.x + 5, 0.08)
        if (self.square_y < 4 and y > 0) or (self.square_y > 0 and y < 0):
            self.square_y += y
            self.y_tween = tween.Tween(tween.EaseSineInOut, (self.square_y - y) * 80 + self.y + 5,
                                           self.square_y * 80 + self.y + 5, 0.08)

    def blit(self):
        if self.x_tween:
            self.x_tween.update()
            # print("X tweening: ", self.x_tween.curr_val)
            self.square_actual_x = self.x_tween.curr_val
        if self.y_tween:
            self.y_tween.update()
            # print("Y tweening: ", self.y_tween.curr_val)
            self.square_actual_y = self.y_tween.curr_val
        screen.blit(self.square_image, (self.square_actual_x, self.square_actual_y))
        screen.blit(self.image, (self.x, self.y))


def gameplay_screen():
    clock = pygame.time.Clock()
    events = pygame.event.get()
    grid = Grid(SIZE[0] // 2 - 405, SIZE[1] - 500)
    while not utils.check_quit(events):
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        clock.tick(60)
        screen.fill((0, 0, 0))

        for event in events:
            if event.type == pygame.KEYDOWN:
                print(event.dict)
                if event.dict['key'] == pygame.K_UP:
                    grid.move_square(0, -1)
                    print("wow")
                if event.dict['key'] == pygame.K_DOWN:
                    grid.move_square(0, 1)
                if event.dict['key'] == pygame.K_LEFT:
                    grid.move_square(-1, 0)
                if event.dict['key'] == pygame.K_RIGHT:
                    grid.move_square(1, 0)

        grid.blit()
        pygame.display.update()

    return -1
