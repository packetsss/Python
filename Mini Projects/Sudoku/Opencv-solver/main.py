import cv2
import sys
from time import time
import matplotlib.pyplot as plt
from Sudoku_solver import solve
from Sudoku_extractor import extract_sudoku


def output(a):
    sys.stdout.write(str(a))


def display_sudoku(sudoku):
    for i in range(9):
        for j in range(9):
            cell = sudoku[i][j]
            if cell == 0 or isinstance(cell, set):
                output('.')
            else:
                output(cell)
            if (j + 1) % 3 == 0 and j < 8:
                output(' |')

            if j != 8:
                output('  ')
        output('\n')
        if (i + 1) % 3 == 0 and i < 8:
            output("--------+----------+---------\n")


def show_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.show()


def main(image_path):
    image = extract_sudoku(image_path)
    show_image(image)
    grid = extract_number(image)
    print('Sudoku:')
    display_sudoku(grid.tolist())
    solution = solve(grid).ai()
    print('Solution:')
    #    print(solution)
    display_sudoku(solution.tolist())


def convert_sec_to_hms(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%08d" % (hour, minutes, seconds)


if __name__ == '__main__':
    #    image_path = 'images/sudoku.jpg'
    #    main(image_path)

    start_time = time()
    main("src/board.jpeg")
    print("TAT: ", round(time() - start_time, 3))

