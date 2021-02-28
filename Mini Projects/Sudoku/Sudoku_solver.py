import Sudoku_interface as ss
import numpy as np


class solve:
    def __init__(self, p):
        self.puzzle = np.array(p)
        self.difficulty = 0
        self.ai()

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
        length = 2
        while length <= 5:
            for i in range(9):
                for j in range(9):
                    if len(str(self.puzzle[i, j])) == length:

                        for k in str(self.puzzle[i, j]):
                            row = self.puzzle[i, :]
                            cln = self.puzzle[:, j]
                            ii, jj = self.mn_index(i, j)
                            if len(str(self.puzzle[i, j])) != length:
                                break
                            elif str("".join(map(str, row))).count(k) == 1 or str("".join(map(str, cln))).count(k) == 1 \
                                    or str("".join(map(str, self.mini_nine()[ii, :]))).count(k) == 1:

                                self.puzzle[i, :] = [int(i) for i in
                                                     [s.replace(k, '') for s in list(map(str, row))]]
                                self.puzzle[:, j] = [int(i) for i in
                                                     [s.replace(k, '') for s in list(map(str, cln))]]
                                self.puzzle[i, j] = int(k)
                                self.mini_nine()

            length += 1

    def ai(self):
        self.init()

        while sum(sum(self.puzzle)) != 405 and self.difficulty < 50:
            self.unique()
            self.difficulty += 1

        return self.puzzle, self.difficulty


a, d = solve(ss.interface().foundation()).ai()
print(a, "\n", d)
print(np.array(ss.interface(solution=True).foundation()))
#solve(ss.interface().print_board(a.tolist()))
