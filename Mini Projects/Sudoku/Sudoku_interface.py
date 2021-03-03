from random import sample
import ast


class interface:

    def __init__(self, solution=False, random=False):
        self.shuffle = random
        self.solution = solution
        self.base = 3
        self.side = self.base * self.base

    def pattern(self, r, c):
        return (self.base * (r % self.base) + r // self.base + c) % self.side

    def foundation(self):
        if not self.shuffle:
            with open("puzzle1.txt") as f:
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
            def shuffle(s):
                return sample(s, len(s))

            rBase = range(self.base)
            rows = [g * self.base + r for g in shuffle(rBase) for r in shuffle(rBase)]
            cols = [g * self.base + c for g in shuffle(rBase) for c in shuffle(rBase)]
            nums = shuffle(range(1, self.base * self.base + 1))

            board = [[nums[self.pattern(r, c)] for c in cols] for r in rows]
            board1 = [[nums[self.pattern(r, c)] for c in cols] for r in rows]

            squares = self.side * self.side
            empties = int(squares * (2 / 5))
            for p in sample(range(squares), empties):
                board[p // self.side][p % self.side] = 0

            with open("puzzle.txt", "a") as f:
                d = {"puzzle": board,
                     "solution": board1}
                print(d, file=f)

            if self.solution:
                return board1
            else:
                return board

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
    print(interface(solution=False).foundation())


if "__main__" == __name__:
    main()
