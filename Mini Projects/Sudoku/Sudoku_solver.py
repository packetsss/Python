import Sudoku_interface as ss
import numpy as np
from timeit import default_timer as timer


class solve:
    def __init__(self, p):
        self.puzzle = np.array(p)
        self.difficulty = 0
        self.changes = 0

    def mini_nine(self):
        arr = np.array([list(np.reshape(self.puzzle[i:i + 3, j:j + 3], (1, 9))[0])
                        for i in range(0, 7, 3) for j in range(0, 7, 3)])
        return arr

    @staticmethod
    def mn_index(i, j):
        ii = (int(np.floor(i / 3)) * 3) + int(np.floor(j / 3))
        jj = (i % 3) * 3 + (j % 3)

        return ii, jj

    def init(self):
        l = ""
        for i in range(9):
            for j in range(9):
                row = self.puzzle[i, :]
                cln = self.puzzle[:, j]
                ii, jj = self.mn_index(i, j)

                if self.puzzle[i, j] == 0:
                    for k in range(1, 10):
                        if k not in row and k not in cln \
                                and k not in self.mini_nine()[ii, :]:
                            l += str(k)

                    self.mini_nine()[ii, jj] = int(l)
                    self.puzzle[i, j] = int(l)
                    l = ""

    def unique(self):
        for i in range(9):
            for j in range(9):
                if len(str(self.puzzle[i, j])) > 2:
                    for k in str(self.puzzle[i, j]):
                        row = self.puzzle[i, :]
                        cln = self.puzzle[:, j]
                        ii, jj = self.mn_index(i, j)

                        if (str("".join(map(str, row))).count(k) == 1 or str("".join(map(str, cln))).count(k) == 1
                            or str("".join(map(str, self.mini_nine()[ii, :]))).count(k) == 1) \
                                and len(str(self.puzzle[i, j])) > 1:
                            self.puzzle[i, :] = [int(i) for i in
                                                 [s.replace(k, '') for s in list(map(str, row))]]
                            self.puzzle[:, j] = [int(i) for i in
                                                 [s.replace(k, '') for s in list(map(str, cln))]]
                            self.puzzle[i, j] = int(k)
                            self.mini_nine()
                            self.changes += 1

    def ai(self):
        start = timer()
        self.init()

        while True:
            self.changes = 0
            self.unique()
            self.difficulty += 1
            if self.changes == 0:
                break
        end = timer()

        return self.puzzle, self.difficulty, end - start


def main():
    a, d, time = solve(ss.interface(random=False).foundation()).ai()
    print(f"Time consumed: {round(time, 5)}\nDifficulty: {d}\nSolver:\n{a}\n")
    print(f"Solution:\n{np.array(ss.interface(solution=True).foundation())}")
    # solve(ss.interface().print_board(a.tolist()))


if "__main__" == __name__:
    main()
