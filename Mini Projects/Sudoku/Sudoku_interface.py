from random import sample
import random
import ast


class interface:

    def __init__(self, solution=False, random=False):
        self.shuffle = random
        self.solution = solution
        self.base = 3
        self.side = self.base * self.base

    def foundation(self):
        if not self.shuffle:
            with open("src\\puzzle1.txt") as f:
                for line in f:
                    if len(line) < 10:
                        break
                    last_line = line

            a = ast.literal_eval(last_line)
            if not self.solution:
                return a["puzzle"]
            else:
                return a["solution"]
        else:
            with open("src\\puzzle1.txt") as f:
                ct = 0
                for l in f:
                    ct += 1
                rand = random.randint(1, ct)
            with open("src\\puzzle1.txt") as f:
                for i, line in enumerate(f):
                    if i == rand + 1:
                        l = line
                        break
            a = ast.literal_eval(l)
            if not self.solution:
                return a["puzzle"]
            else:
                return a["solution"]

    def expandLine(self, line):
        return line[0] + line[5:9].join([line[1:5] * (self.base - 1)] * self.base) + line[9:13]

    def print_board(self, board):
        line0 = self.expandLine("╔═══╤═══╦═══╗")
        line1 = self.expandLine("║ . │ . ║ . ║")
        line2 = self.expandLine("╟───┼───╫───╢")
        line3 = self.expandLine("╠═══╪═══╬═══╣")
        line4 = self.expandLine("╚═══╧═══╩═══╝")

        symbol = " 1234567890"
        nums = [[""] + [symbol[n] for n in row] for row in board]

        print(line0)
        for r in range(1, self.side + 1):
            print("".join(n + s for n, s in zip(nums[r - 1], line1.split("."))))
            print([line2, line3, line4][(r % self.side == 0) + (r % self.base == 0)])


def main():
    interface(solution=True).print_board(interface().foundation())


if "__main__" == __name__:
    main()
