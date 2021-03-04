import os
import sys
import pygame as pg
import numpy as np

from Sudoku_interface import interface
from Sudoku_solver import solve

pg.init()
screen_x = 900
screen_y = 750
screen_size = screen_x, screen_y
multiplier = min(screen_size) // 10
screen = pg.display.set_mode(screen_size)
clock = pg.time.Clock()

font = pg.font.SysFont("", size=80)
small_font = pg.font.SysFont('Corbel', 35)
text = small_font.render('quit', True, pg.Color("Yellow"))


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


with HiddenPrints():
    number_grid = np.array(interface().foundation())
    a, _, _ = solve(number_grid).ai()


def draw_background():
    m = multiplier * 9
    screen.fill(pg.Color("White"))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(15, 15, m, m), 7, border_radius=20)
    for i in range(1, 9):
        line_width = 3 if i % 3 > 0 else 7
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(((i * multiplier) + 15), 15),
                     pg.Vector2(((i * multiplier) + 15), m + 10), line_width)
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(15, ((i * multiplier) + 15)),
                     pg.Vector2(m + 10, ((i * multiplier) + 15)), line_width)


def draw_numbers(n_g):
    offset = 38
    for row in range(9):
        for col in range(9):
            output = n_g[row][col] if n_g[row][col] != 0 else ""
            n_text = font.render(str(output), True, pg.Color("black"))
            screen.blit(n_text, pg.Vector2((col * multiplier) + offset, (row * multiplier) + offset - 10))


def draw_button(button, screen1):
    """Draw the button rect and the text surface."""
    pg.draw.rect(screen1, button['color'], button['rect'])
    screen1.blit(button['text'], button['text rect'])


def create_button(x, y, w, h, text1, callback):
    """A button is a dictionary that contains the relevant data.

    Consists of a rect, text surface and text rect, color and a
    callback function.
    """
    # The button is a dictionary consisting of the rect, text,
    # text rect, color and the callback function.
    text_surf = pg.font.Font(None, 25).render(text1, True, (255, 255, 255))
    button_rect = pg.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': pg.Color('dodgerblue4'),
        'callback': callback,
    }
    return button


def game_loop(grid, solved_grid):
    def solved():
        nonlocal cond
        cond = True

    def unsolved():
        nonlocal cond
        cond = False

    def shuffle():
        nonlocal grid, solved_grid
        with HiddenPrints():
            grid = interface(random=True).foundation()
            solved_grid, _, time = solve(grid).ai()
        print(f"Time consumed while calculating solution: {round(time, 3)}")

    cond = False
    button1 = create_button(screen_x * 0.8, 50, 150, 40, 'Show solution!', solved)
    button2 = create_button(screen_x * 0.8, 100, 150, 40, 'Hide solution!', unsolved)
    button3 = create_button(screen_x * 0.8, 150, 150, 40, 'Shuffle puzzle!', shuffle)
    button_list = [button1, button2, button3]

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.MOUSEBUTTONDOWN:
                for button in button_list:
                    if event.button == 1:
                        if button['rect'].collidepoint(event.pos):
                            button['callback']()
            elif event.type == pg.MOUSEMOTION:
                for button in button_list:
                    if button['rect'].collidepoint(event.pos):
                        button['color'] = pg.Color('dodgerblue4')
                    else:
                        button['color'] = pg.Color('dodgerblue1')

        if cond:
            board = solved_grid
        else:
            board = grid

        draw_background()
        draw_numbers(board)

        for button in button_list:
            draw_button(button, screen)

        clock.tick(30)
        pg.display.update()



game_loop(number_grid, a)

pg.display.quit()
pg.quit()
sys.exit()
