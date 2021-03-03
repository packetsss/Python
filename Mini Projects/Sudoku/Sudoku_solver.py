import Sudoku_interface as ss
import numpy as np
from timeit import default_timer as timer
import random
from copy import deepcopy


class solve:
    def __init__(self, p):
        self.puzzle = np.array(p)
        self.puzzle1 = np.array(p)
        self.attempts = 0
        self.changes = 0
        self.i = 0
        self.j = 0

    @staticmethod
    def mini_nine(puzzle):
        arr = np.array([list(np.reshape(puzzle[i:i + 3, j:j + 3], (1, 9))[0])
                        for i in range(0, 7, 3) for j in range(0, 7, 3)])
        return arr

    @staticmethod
    def mn_index(i, j):
        ii = (int(np.floor(i / 3)) * 3) + int(np.floor(j / 3))
        jj = (i % 3) * 3 + (j % 3)

        return ii, jj

    def mn_index_block(self, i, j):
        return self.puzzle[int(i / 3) * 3:int(i / 3) * 3 + 3, int(j / 3) * 3:int(j / 3) * 3 + 3]

    def init(self, puz):
        p = deepcopy(puz)
        l = ""
        for i in range(9):
            for j in range(9):

                if len(str(puz[i, j])) > 1:
                    puz[i, j] = 0

                row = puz[i, :]
                cln = puz[:, j]
                ii, jj = self.mn_index(i, j)
                boo = False
                if puz[i, j] == 0:
                    for k in range(1, 10):
                        if k not in row and k not in cln \
                                and k not in self.mini_nine(self.puzzle1)[ii, :]:
                            l += str(k)
                            boo = True
                    if not boo:
                        self.puzzle1 = deepcopy(p)
                        self.mini_nine(self.puzzle1)
                        print(f"Failed at init")
                        return False
                    self.mini_nine(self.puzzle1)
                    puz[i, j] = int(l)
                    l = ""
        self.puzzle1 = deepcopy(puz)
        return True

    def unique(self, p):
        for i in range(9):
            for j in range(9):
                if len(str(p[i, j])) > 1:
                    for k in str(p[i, j]):
                        row = p[i, :]
                        cln = p[:, j]
                        ii, jj = self.mn_index(i, j)

                        if (str("".join(map(str, row))).count(k) == 1 or str("".join(map(str, cln))).count(k) == 1
                            or str("".join(map(str, self.mini_nine(p)[ii, :]))).count(k) == 1) \
                                and len(str(p[i, j])) > 1:
                            try:
                                p[i, :] = [int(i) for i in
                                           [s.replace(k, '') for s in list(map(str, row))]]

                                p[:, j] = [int(i) for i in
                                           [s.replace(k, '') for s in list(map(str, cln))]]
                            except ValueError:
                                print(f"Failed at unique\ni: {i}, j: {j}")
                                return False

                            p[i, j] = int(k)
                            self.mini_nine(p)
                            self.changes += 1
        return True

    def elimination(self, p):
        for i in range(9):
            for j in range(9):
                if len(str(p[i, j])) > 1:

                    l = [str(p[i, j])]
                    for k in range(9):
                        if len(str(p[i, :][k])) < 2 or k == j:
                            continue

                        if set(map(int, str(str(p[i, :][k])))). \
                                issubset(set(map(int, str(p[i, j])))):
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

                        if set(map(int, str(str(p[:, j][kk])))). \
                                issubset(set(map(int, str(p[i, j])))):
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

                    l = []
                    for s in range(3):
                        for ss in range(3):
                            if len(str(self.mn_index_block(i, j)[s, ss])) < 2:
                                continue

                            if set(map(int, str(str(self.mn_index_block(i, j)[s, ss])))). \
                                    issubset(set(map(int, str(self.puzzle[i, j])))):
                                l.append(str(self.mn_index_block(i, j)[s, ss]))

                            if 1 < len(l) == len(max(l, key=len)):

                                for q1 in range(3):
                                    for q2 in range(3):
                                        qq2 = str(self.mn_index_block(i, j)[q1, q2])

                                        for q3 in max(l, key=len):
                                            if qq2 not in l:
                                                qq2 = int(str(qq2).replace(q3, ''))
                                        self.mn_index_block(i, j)[q1, q2] = qq2
        return True

    def try_insert(self, length=2):
        for i in range(9):
            for j in range(9):
                if len(str(self.puzzle[i, j])) == length:
                    # print(random.choice([int(i) for i in str(self.puzzle[i, j])]))
                    self.puzzle[i, j] = random.choice([int(i) for i in str(self.puzzle[i, j])])
                    return None

    def check(self, p):
        for i in range(9):
            a = [i for i in p[i, :] if len(str(i)) == 1]
            if sorted(list(set(a))) != sorted(a):
                print("Failed at check: ROW")
                print(self.puzzle1)
                return False

            b = [i for i in p[:, i] if len(str(i)) == 1]
            if sorted(list(set(b))) != sorted(b):
                print("Failed at check: COLUMN")
                return False

            c = [i for i in self.mini_nine(p)[i, :] if len(str(i)) == 1]
            if sorted(list(set(c))) != sorted(c):
                print("Failed at check: MN_NINE")
                return False
            return True

    def check_v2(self, i, j, k):

        ii, jj = self.mn_index(i, j)
        if k in self.puzzle1[i, :]:
            print("Failed at check_v2: ROW")
            return False
        if k in self.puzzle1[:, j]:
            print("Failed at check_v2: COLUMN")
            return False
        if k in self.mini_nine(self.puzzle1)[ii, :]:
            print("Failed at check_v2: MN_NINE")
            return False
        return True

    def out(self):
        def minimum_length(p):
            length = 10
            for ii in range(9):
                for jj in range(9):
                    if 1 < len(str(p[ii, jj])) < length:
                        length = len(str(p[ii, jj]))
            return length

        # l = minimum_length(self.puzzle1)
        for i in range(9):
            for j in range(9):
                if len(str(self.puzzle1[i, j])) > 1:
                    return i, j

        return False

    def try_v2(self):
        p = deepcopy(self.puzzle1)
        self.attempts += 1
        if not self.out():
            return True
        else:
            i, j = self.out()

        for k in [int(k) for k in str(self.puzzle1[i, j])]:
            print(f"Now inserting \"{k}\" at ({i}, {j})")
            self.puzzle1[i, j] = k
            print(f"Puzzle after Insert: \n{self.puzzle1}")

            if not self.init(self.puzzle1) or not self.unique(self.puzzle1) \
                    or not self.elimination(self.puzzle1) or not self.check(self.puzzle1):
                self.puzzle1 = deepcopy(p)
                print("Return to previous puzzle version\n", self.puzzle1)
                continue
            else:
                print("Now proceed Deeper: Every test passed!")
                print(f"Puzzle after testing: \n{self.puzzle1}")

                if self.try_v2():
                    return True
                else:
                    self.puzzle1 = deepcopy(p)
        self.puzzle1 = deepcopy(p)
        print("Back Tracking")
        print(f"i: {i} j: {j}")
        return False

    def ai(self):
        start = timer()
        self.init(self.puzzle1)
        self.unique(self.puzzle1)
        self.elimination(self.puzzle1)
        self.try_v2()

        if not self.check(self.puzzle1) or sum(sum(self.puzzle1)) != 405:
            print(sum(sum(self.puzzle1)))
            print(f"\nSolving Failed!\n")
        else:
            print(sum(sum(self.puzzle1)))
            print("\nSolving Success!\n")
        end = timer()

        return self.puzzle1, self.attempts, end - start


def main():
    a, d, time = solve(ss.interface().foundation()).ai()
    print(f"Puzzle:\n{np.array(ss.interface().foundation())}")
    print(f"Time consumed: {round(time, 5)}\nAttempts: {d}\nSolver:\n{a}\n")
    # print(f"Solution:\n{np.array(ss.interface(solution=True).foundation())}")
    solve(ss.interface().print_board(a.tolist()))


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
