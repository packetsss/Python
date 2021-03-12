import pygame as pg
from queue import PriorityQueue
import sys
from timeit import default_timer as timeit
import numpy as np


WIDTH = 800
WIN = pg.display.set_mode((WIDTH, WIDTH))
pg.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, tot_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = tot_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def is_end1(self):
        return self.color == TURQUOISE

    def is_empty(self):
        return self.color == WHITE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        rect = pg.Rect(self.x + 1, self.y + 1, self.width - 1, self.width - 1)
        pg.draw.rect(win, self.color, rect)
        pg.display.update(rect)

    def display_distance(self, win, f_score, font):
        rect = pg.Rect(self.x + 1, self.y + 1, self.width - 1, self.width - 1)
        txt_surf = font.render(str(f_score), True, BLACK)
        win.blit(txt_surf, rect)
        pg.display.update(rect)

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Down
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Up
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Right
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
        # Left

        #---Diagonal distance---#

        if (self.row > 0 and self.col > 0) and not grid[self.row - 1][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col - 1])
        # top-left
        if (self.row > 0 and self.col < self.total_rows - 1) and not grid[self.row - 1][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col + 1])
        # top-right
        if (self.row < self.total_rows - 1 and self.col > 0) and not grid[self.row + 1][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col - 1])
        # bot-left
        if (self.row < self.total_rows - 1 and self.col < self.total_rows - 1) \
                and not grid[self.row + 1][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col + 1])
        # bot-right

    def __lt__(self, other):
        # the other spot is greater than this spot
        return False


def heuristic(p1, p2):
    # row, col, Manhattan distance(no diagonal)
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, win):
    while current in came_from:
        current.draw(win)
        current = came_from[current]
        current.make_path()


def algorithm(win, grid, start, end):
    ct = 0
    open_set = PriorityQueue()
    # get minimum element from this queue
    open_set.put((0, ct, start))
    # add F score, ct is tie breaker

    came_from = {}
    # keep track of the path

    g_score = {spot: float("inf") for row in grid for spot in row}
    # dictionary comprehension, keep track of shortest distance from start node to this node
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
    # keep track predicted distance from current node to end node
    f_score[start] = heuristic(start.get_pos(), end.get_pos())
    # make an estimate distance between start and end

    open_set_hash = {start}
    # copy the queue, help us to see if anything in the open_set

    while not open_set.empty():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        # pop out the queue to sync

        if current == end:
            reconstruct_path(came_from, end, win)
            end.make_end()
            return "Total distance: " + str(f)

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                # if found closer path
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                f, g = g_score[neighbor], f_score[neighbor] - temp_g_score
                # update the came_from, f score, g score

                if neighbor not in open_set_hash:
                    ct += 1
                    open_set.put((f_score[neighbor], ct, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        current.draw(win)
        # update the current node to the screen

        '''current.display_distance(win, f)'''

        if current != start:
            a = came_from[current]
            a.make_closed()
            a.draw(win)


            # current.draw(win)

        pg.time.Clock().tick(1000)
    return "Cannot find path"


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    win.fill(WHITE)
    gap = width // rows
    for i in range(rows):
        pg.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pg.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
    pg.display.update()


def mouse_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    pg.init()
    font = pg.font.Font(None, 15)
    ROWS = 50
    grid = make_grid(ROWS, width)

    draw_grid(win, ROWS, width)

    start, end, run = None, None, True

    while run:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if pg.mouse.get_pressed()[0]:
                # left mouse
                x, y = pg.mouse.get_pos()
                row, col = mouse_pos((x, y), ROWS, width)
                spot = grid[row][col]

                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()
                spot.draw(win)

            elif pg.mouse.get_pressed()[2]:
                # right mouse
                pos = pg.mouse.get_pos()
                row, col = mouse_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
                spot.draw(win)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    f_score = algorithm(win, grid, start, end)
                    print(f"\n{f_score}\n")

                if event.key == pg.K_c:
                    start, end = None, None
                    grid = make_grid(ROWS, width)
                    draw_grid(win, ROWS, width)

    pg.quit()
    sys.exit()


if "__main__" == __name__:
    main(WIN, WIDTH)
