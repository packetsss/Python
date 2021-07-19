import os
import time
import random
import threading
import numpy as np
from msvcrt import getch


class Node:
    def __init__(self, data=None, next_node=None, previous_node=None, direction="right", size=None):
        if data is None:
            data = [0, 0]

        self.data = data  # format: [1, 1]
        self.next = next_node
        self.prev = previous_node
        self.direction = direction
        self.s = size

    def move(self):
        if self.direction == "right":
            self.data[1] += 1
            if self.data[1] > self.s:
                self.data[1] = 0
        elif self.direction == "left":
            self.data[1] -= 1
            if self.data[1] < 0:
                self.data[1] = self.s
        elif self.direction == "up":
            self.data[0] -= 1
            if self.data[0] < 0:
                self.data[0] = self.s
        elif self.direction == "down":
            self.data[0] += 1
            if self.data[0] > self.s:
                self.data[0] = 0

    def peak_next_move(self):
        if self.direction == "right":
            return (self.data[0], 0) if self.data[1] + 1 > self.s else (self.data[0], self.data[1] + 1)
        elif self.direction == "left":
            return (self.data[0], self.s) if self.data[1] - 1 < 0 else (self.data[0], self.data[1] - 1)
        elif self.direction == "up":
            return (self.s, self.data[1]) if self.data[0] - 1 < 0 else (self.data[0] - 1, self.data[1])
        elif self.direction == "down":
            return (0, self.data[1]) if self.data[0] + 1 > self.s else (self.data[0] + 1, self.data[1])

    def get_next(self):
        return self.next

    def set_next(self, n):
        self.next = n

    def get_prev(self):
        return self.prev

    def set_prev(self, p):
        self.prev = p

    def get_data(self):
        return self.data

    def set_data(self, d):
        self.data = d


class Snake:
    def __init__(self, grid, size):
        self.s = size - 1
        self.grid = grid
        self.root = Node(size=self.s)
        self.tail = self.root
        self.size = 0

    def get_size(self):
        return self.size

    def push(self):
        this_node = self.root
        data = this_node.get_data().copy()
        while this_node.get_next() is not None:
            this_node = this_node.get_next()
            data = this_node.get_data().copy()

        if this_node.direction == "left":
            data[1] = (data[1] + 1) if data[1] < self.s else 0
        elif this_node.direction == "right":
            data[1] = (data[1] - 1) if data[1] > 0 else self.s
        elif this_node.direction == "up":
            data[0] = (data[0] + 1) if data[0] < self.s else 0
        elif this_node.direction == "down":
            data[0] = (data[0] - 1) if data[0] > 0 else self.s

        self.grid[data[0], data[1]] = "X"
        # print(data)
        new_node = Node(data, None, this_node, this_node.direction, self.s)
        this_node.set_next(new_node)
        self.tail = new_node

        self.size += 1

    def move_snake(self, direction=None):
        this_node = self.root

        x, y = this_node.peak_next_move()
        if self.grid[x, y] == "+":
            self.push()

        if self.grid[x, y] == "X":
            return False

        while this_node is not None:
            last_x, last_y = this_node.get_data()
            self.grid[last_x, last_y] = " "

            this_node.move()

            x, y = this_node.get_data()
            self.grid[x, y] = "X"

            this_node = this_node.get_next()

        if direction is None:
            direction = self.root.direction
        self.change_direction(direction)
        return True

    def change_direction(self, direction):
        this_node = self.tail

        while this_node.prev is not None:
            this_node.direction = this_node.prev.direction
            this_node = this_node.prev

        this_node.direction = direction

    def display(self):
        lst = []
        this_node = self.root
        while this_node:
            lst.append([this_node.data, this_node.direction])
            this_node = this_node.next
        print("\n", lst)


def game(size):
    def detect_key():
        while 1:
            nonlocal key, last_key, moved
            key = ord(getch())
            if last_key != key:
                if key in key_dict:
                    moved = True
                    snake.move_snake(key_dict[key])
                    print_board(grid)
            last_key = key

    def print_board(board):
        # print(board, "\n" * 3, end="\r")
        print("\n" * 3)
        for i in range(size):
            print("|", " | ".join(board[i, :]), end=" |\n")

    key, last_key, moved = None, None, False
    trd = threading.Thread(target=detect_key, daemon=False)
    trd.start()

    grid = [[" " for _ in range(size)] for _ in range(size)]
    grid = np.array(grid, dtype=object)
    snake = Snake(grid, size)
    key_dict = {
        # 77>  75<  72/\  80\/
        72: "up",
        80: "down",
        77: "right",
        75: "left"
    }
    ct, rand_range = 0, 2
    rand_value = random.randint(0, rand_range)
    while 1:
        if not moved:
            if not snake.move_snake():
                print("\nGame over :p", end="\r")
                os._exit(0)
            print_board(grid)
        else:
            moved = False
        # snake.display()

        if ct >= rand_value:
            rand_range += 1
            rand_value = random.randint(0, rand_range)

            rand_x, rand_y = random.randint(0, size - 1), random.randint(0, size - 1)
            grid[rand_x, rand_y] = "+"
            ct = 0
        ct += 1

        time.sleep(0.8)


def main():
    game(12) # grid dimension


if "__main__" == __name__:
    main()
