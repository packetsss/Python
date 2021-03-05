import Sudoku_interface as ss
import numpy as np
from timeit import default_timer as timer
import random
from copy import deepcopy
import sys


class solve:
    def __init__(self, p):
        self.puzzle, self.attempts, self.sets = np.array(p), 0, list(range(1, 10))

    @staticmethod
    def mini_nine(puzzle):
        return np.array([(np.reshape(puzzle[i:i + 3, j:j + 3], (1, 9))[0])
                         for i in range(0, 7, 3) for j in range(0, 7, 3)])

    @staticmethod
    def mn_index(i, j):
        return (int(np.floor(i / 3)) * 3) + int(np.floor(j / 3)), (i % 3) * 3 + (j % 3)

    @staticmethod
    def mn_index_block(i, j):
        return int(i / 3) * 3, int(i / 3) * 3 + 3, int(j / 3) * 3, int(j / 3) * 3 + 3

    def init(self, p):
        p_copy = deepcopy(p)
        for i in range(9):
            for j in range(9):

                if len(str(p[i, j])) > 1:
                    p[i, j] = 0

                if p[i, j] == 0:
                    row = p[i, :]
                    col = p[:, j]
                    a, a3, b, b3 = self.mn_index_block(i, j)
                    mn_puz = np.reshape(self.puzzle[a:a3, b:b3], (1, 9))[0]

                    try:
                        p[i, j] = int("".join(map(str, set(self.sets)
                                                  .difference(set(row))
                                                  .difference(set(col))
                                                  .difference(set(mn_puz)))))
                    except ValueError:
                        self.puzzle = deepcopy(p_copy)
                        print(f"Failed at init")
                        return False
        return True

    def unique(self, p):
        for i in range(9):
            for j in range(9):
                if len(str(p[i, j])) > 1:
                    for k in str(p[i, j]):
                        row = p[i, :]
                        cln = p[:, j]

                        a, a3, b, b3 = self.mn_index_block(i, j)
                        mn_puz = np.reshape(self.puzzle[a:a3, b:b3], (1, 9))[0]

                        if len(str(p[i, j])) > 1 and ("".join(map(str, row)).count(k) == 1 or
                                                      "".join(map(str, cln)).count(k) == 1 or
                                                      "".join(map(str, mn_puz)).count(k) == 1):
                            try:
                                p[i, :] = [int(s.replace(k, '')) for s in list(map(str, row))]
                                p[:, j] = [int(s.replace(k, '')) for s in list(map(str, cln))]
                            except ValueError:
                                print(f"Failed at unique\ni: {i}, j: {j}")
                                return False

                            p[i, j] = int(k)

        return True

    @staticmethod
    def elimination(p):
        for i in range(9):
            for j in range(9):
                if len(str(p[i, j])) > 1:

                    l = [str(p[i, j])]
                    for k in range(9):
                        if len(str(p[i, :][k])) < 2 or k == j:
                            continue

                        if set(str(p[i, :][k])).issubset(set(str(p[i, j]))):
                            l.append(str(p[i, :][k]))

                        if 1 < len(l) == len(max(l, key=len)):

                            ll = []
                            for s in p[i, :]:
                                s = str(s)
                                for ss in max(l, key=len):
                                    if s not in l:
                                        s = s.replace(ss, '')
                                ll.append(s)
                            try:
                                p[i, :] = np.array([int(i) for i in ll])
                            except ValueError:
                                return False

                    l = [str(p[i, j])]
                    for kk in range(9):
                        if len(str(p[:, j][kk])) < 2 or kk == i:
                            continue

                        if set(str(p[:, j][kk])).issubset(set(str(p[i, j]))):
                            l.append(str(p[:, j][kk]))

                        if 1 < len(l) == len(max(l, key=len)):

                            ll = []
                            for s in p[:, j]:
                                s = str(s)
                                for ss in max(l, key=len):
                                    if s not in l:
                                        s = s.replace(ss, '')
                                ll.append(s)
                            try:
                                p[:, j] = np.array([int(i) for i in ll])
                            except ValueError:
                                return False
        return True

    def try_insert(self, length=2):
        for i in range(9):
            for j in range(9):
                if len(str(self.puzzle[i, j])) == length:
                    self.puzzle[i, j] = random.choice([int(i) for i in str(self.puzzle[i, j])])
                    return None

    def check(self, p):
        for i in range(9):
            row = [i for i in p[i, :] if len(str(i)) == 1]
            if len(set(row)) != len(row):
                print(f"Failed at check: ROW")
                return False

            col = [i for i in p[:, i] if len(str(i)) == 1]
            if len(set(col)) != len(col):
                print("Failed at check: COLUMN")
                return False

            a1, a3, b1, b3 = self.mn_index_block(i, i % 3 * 3)
            mn_puz = np.reshape(self.puzzle[a1:a3, b1:b3], (1, 9))[0]
            mn_row = [i for i in mn_puz if len(str(i)) == 1]
            if len(set(mn_row)) != len(mn_row):
                print("Failed at check: MN_NINE")
                return False
            return True

    def check_v2(self, i, j, k):

        ii, jj = self.mn_index(i, j)
        if k in self.puzzle[i, :]:
            print("Failed at check_v2: ROW")
            return False
        if k in self.puzzle[:, j]:
            print("Failed at check_v2: COLUMN")
            return False
        if k in self.mini_nine(self.puzzle)[ii, :]:
            print("Failed at check_v2: MN_NINE")
            return False
        return True

    def out(self):
        def minimum_length(p):
            length = 10
            for ii in range(9):
                for jj in range(9):
                    if len(str(p[ii, jj])) == 2:
                        return 2
                    if 1 < len(str(p[ii, jj])) < length:
                        length = len(str(p[ii, jj]))
            return length

        min_l = minimum_length(self.puzzle)
        for i in range(9):
            for j in range(9):
                if min_l == len(str(self.puzzle[i, j])):
                    return i, j

        return False

    def try_v2(self):
        p = deepcopy(self.puzzle)
        self.attempts += 1
        if not self.out():
            if sum(sum(self.puzzle)) == 405:
                return True
            else:
                return False
        else:
            i, j = self.out()

        for k in [int(k) for k in str(self.puzzle[i, j])]:
            # print(f"Now inserting \"{k}\" at ({i}, {j})")
            self.puzzle[i, j] = k

            if not self.init(self.puzzle) or not self.unique(self.puzzle) or not self.elimination(self.puzzle) \
                    or not self.check(self.puzzle):
                self.puzzle = deepcopy(p)
                # print("Return to previous puzzle version")
                continue
            else:
                # print("Now proceed Deeper: Every test passed!")

                if self.try_v2():
                    return True
                else:
                    self.puzzle = deepcopy(p)
        print(f"Back Tracking to | i: {i} | j: {j}")
        return False

    def ai(self):
        start = timer()
        self.init(self.puzzle)
        print(self.puzzle)
        self.try_v2()
        end = timer()
        if not self.check(self.puzzle) or sum(sum(self.puzzle)) != 405:
            print(f"\nSolving Failed!\n".upper())
        else:
            print("\nSolving Success!\n".upper())

        return self.puzzle, self.attempts, end - start


def main():
    a, d, time = solve(ss.interface().foundation()).ai()
    # print(f"Puzzle:\n{np.array(ss.interface().foundation())}")
    print(f"Solver:\n{a}\n\nTime consumed: {round(time, 5)}\nAttempts: {d}")
    # solve(ss.interface().print_board(a.tolist()))


if "__main__" == __name__:
    main()

'''
Stats:

Naive recursive method:
Time consumed: 99.91675
Attempts: 478556

Naive recursive and Unique method:
Time consumed: 55.27906
Attempts: 251150

Naive recursive and Unique and Elimination method:
Time consumed: 53.99089
Attempts: 251150
# did not have affect

Recursive implanted with Unique and Elimination method:
Time consumed: 1.81004
Attempts: 31


'''
