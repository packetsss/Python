import Sudoku_interface as ss
import numpy as np
from timeit import default_timer as timer
import random
from copy import deepcopy


class solve:
    def __init__(self, p):
        self.puzzle = np.array(p)
        self.puzzle1 = np.array(p)
        self.difficulty = 0
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
        l = ""
        for i in range(9):
            for j in range(9):
                row = puz[i, :]
                cln = puz[:, j]
                ii, jj = self.mn_index(i, j)

                if puz[i, j] == 0:
                    for k in range(1, 10):
                        if k not in row and k not in cln \
                                and k not in self.mini_nine(self.puzzle1)[ii, :]:
                            l += str(k)

                    self.mini_nine(self.puzzle1)[ii, jj] = int(l)
                    puz[i, j] = int(l)
                    l = ""

    def unique(self):
        for i in range(9):
            for j in range(9):
                if len(str(self.puzzle[i, j])) > 1:
                    for k in str(self.puzzle[i, j]):
                        row = self.puzzle[i, :]
                        cln = self.puzzle[:, j]
                        ii, jj = self.mn_index(i, j)

                        if (str("".join(map(str, row))).count(k) == 1 or str("".join(map(str, cln))).count(k) == 1
                            or str("".join(map(str, self.mini_nine(self.puzzle)[ii, :]))).count(k) == 1) \
                                and len(str(self.puzzle[i, j])) > 1:
                            self.puzzle[i, :] = [int(i) for i in
                                                 [s.replace(k, '') for s in list(map(str, row))]]
                            self.puzzle[:, j] = [int(i) for i in
                                                 [s.replace(k, '') for s in list(map(str, cln))]]

                            self.puzzle[i, j] = int(k)
                            self.mini_nine(self.puzzle)
                            self.changes += 1
                else:
                    k = str(self.puzzle[i, j])
                    ii, jj = self.mn_index(i, j)

                    if str("".join(map(str, self.puzzle[i, :]))).count(k) > 1:
                        ll = []
                        for s in self.puzzle[i, :]:
                            s = str(s)
                            if s != k:
                                s = s.replace(k, '')
                            ll.append(s)
                        self.puzzle[i, :] = np.array([int(i) for i in ll])

                    if str("".join(map(str, self.puzzle[:, j]))).count(k) > 1:
                        ll = []
                        for s in self.puzzle[:, j]:
                            s = str(s)
                            if s != k:
                                s = s.replace(k, '')
                            ll.append(s)
                        self.puzzle[:, j] = np.array([int(i) for i in ll])

                    self.mini_nine(self.puzzle)
                    if str("".join(map(str, self.mini_nine(self.puzzle)[ii, :]))).count(k) > 1:
                        for s in range(3):
                            for ss in range(3):
                                if len(str(self.mn_index_block(i, j)[s, ss])) > 1 \
                                        and k in str(self.mn_index_block(i, j)[s, ss]):
                                    self.mn_index_block(i, j)[s, ss] = \
                                        int(str(self.mn_index_block(i, j)[s, ss]).replace(k, ''))

    def elimination(self):
        for i in range(9):
            for j in range(9):
                if len(str(self.puzzle[i, j])) > 1:

                    l = [str(self.puzzle[i, j])]
                    for k in range(9):
                        if len(str(self.puzzle[i, :][k])) < 2 or k == j:
                            continue

                        if set(map(int, str(str(self.puzzle[i, :][k])))). \
                                issubset(set(map(int, str(self.puzzle[i, j])))):
                            l.append(str(self.puzzle[i, :][k]))

                        if 1 < len(l) == len(max(l, key=len)):

                            ll = []
                            for s in self.puzzle[i, :]:
                                s = str(s)
                                for ss in max(l, key=len):
                                    if s not in l:
                                        s = s.replace(ss, '')
                                ll.append(s)
                            self.puzzle[i, :] = np.array([int(i) for i in ll])

                    l = [str(self.puzzle[i, j])]
                    for kk in range(9):
                        if len(str(self.puzzle[:, j][kk])) < 2 or kk == i:
                            continue

                        if set(map(int, str(str(self.puzzle[:, j][kk])))). \
                                issubset(set(map(int, str(self.puzzle[i, j])))):
                            l.append(str(self.puzzle[:, j][kk]))

                        if 1 < len(l) == len(max(l, key=len)):

                            ll = []
                            for s in self.puzzle[:, j]:
                                s = str(s)
                                for ss in max(l, key=len):
                                    if s not in l:
                                        s = s.replace(ss, '')
                                ll.append(s)
                            self.puzzle[:, j] = np.array([int(i) for i in ll])

                    self.mini_nine(self.puzzle)

                    # l = []
                    # for s in range(3):
                    #     for ss in range(3):
                    #         if len(str(self.mn_index_block(i, j)[s, ss])) < 2:
                    #             continue
                    #
                    #         if set(map(int, str(str(self.mn_index_block(i, j)[s, ss])))). \
                    #                 issubset(set(map(int, str(self.puzzle[i, j])))):
                    #             l.append(str(self.mn_index_block(i, j)[s, ss]))
                    #
                    #         if 1 < len(l) == len(max(l, key=len)):
                    #
                    #             for q1 in range(3):
                    #                 for q2 in range(3):
                    #                     qq2 = str(self.mn_index_block(i, j)[q1, q2])
                    #
                    #                     for q3 in max(l, key=len):
                    #                         if qq2 not in l:
                    #                             qq2 = int(str(qq2).replace(q3, ''))
                    #                     self.mn_index_block(i, j)[q1, q2] = qq2

    def try_insert(self, leng=2):
        for i in range(9):
            for j in range(9):
                if len(str(self.puzzle[i, j])) == leng:
                    # print(random.choice([int(i) for i in str(self.puzzle[i, j])]))
                    self.puzzle[i, j] = random.choice([int(i) for i in str(self.puzzle[i, j])])
                    return None

    def check(self):
        l = []
        self.mini_nine(self.puzzle)
        for i in range(9):
            a = [i for i in self.puzzle[i, :] if len(str(i)) == 1]
            l.append(sorted(list(set(a))) == sorted(a))

            a = [i for i in self.puzzle[:, i] if len(str(i)) == 1]
            l.append(sorted(list(set(a))) == sorted(a))

            a = [i for i in self.mini_nine(self.puzzle)[i, :] if len(str(i)) == 1]
            l.append(sorted(list(set(a))) == sorted(a))
        # print(l)
        return all(l)

    def check_v2(self, i, j, k):
        ii, jj = self.mn_index(i, j)
        if k in self.puzzle[i, :]:
            return False
        if k in self.puzzle[:, j]:
            return False
        if k in self.mini_nine(self.puzzle)[ii, :]:
            return False
        print(list(self.puzzle))
        return True
        # self.puzzle[i, j] = k
        # self.mini_nine()
        # for i in range(9):
        #     self.mini_nine()
        #     if len([i for i in self.puzzle[i, :] if i != 0]) != len(set([i for i in self.puzzle[i, :] if i != 0])):
        #         #print(list([i for i in self.puzzle[i, :]]), list(set([i for i in self.puzzle[i, :]])))
        #         self.puzzle[i, j] = 0
        #
        #         return False
        #
        #     if len([i for i in self.puzzle[:, i] if i != 0]) != len(set([i for i in self.puzzle[:, i] if i != 0])):
        #         self.puzzle[i, j] = 0
        #         #print(list([i for i in self.puzzle[:, i]]), list(set([i for i in self.puzzle[:, i]])))
        #
        #         return False
        #
        #     if len([i for i in self.mini_nine()[i, :] if i != 0]) != len(
        #             set([i for i in self.mini_nine()[i, :] if i != 0])):
        #         # print(1)
        #         # print(list([i for i in self.mini_nine()[i, :]]), list(set([i for i in self.mini_nine()[i, :]])))
        #         # print("\n")
        #         self.puzzle[i, j] = 0
        #         return False
        # self.puzzle[i, j] = 0
        # print(self.puzzle)
        # return True

    def out(self):
        for i in range(9):
            for j in range(9):
                if self.puzzle[i, j] == 0:
                    return i, j

        return False

    def try_v2(self):

        self.difficulty += 1
        if not self.out():
            return True
        else:
            i, j = self.out()
        #print([k for k in str(self.puzzle1[i, j])])
        for k in [int(k) for k in str(self.puzzle1[i, j])]:
            if self.check_v2(i, j, k):

                self.puzzle[i, j] = k
                if self.try_v2():
                    return True
                self.puzzle[i, j] = 0
        return False

    def ai(self):
        start = timer()
        self.init(self.puzzle1)
        print(self.puzzle1)

        self.try_v2()
        puzzle1 = deepcopy(self.puzzle)
        puzzle2 = deepcopy(self.puzzle)
        ct = 0

        # while self.difficulty < 50:
        #     print(self.puzzle, "\n")
        #     self.changes = 0
        #
        #     try:
        #         self.elimination()
        #         puzzle3 = deepcopy(self.puzzle)
        #         self.unique()
        #         puzzle4 = deepcopy(self.puzzle)
        #     except ValueError:
        #         # self.puzzle = deepcopy(puzzle1)
        #         pass
        #
        #     if not self.check():
        #         # print(f"\n\n{puzzle1}\n\n{puzzle4}")
        #         print("\n", f"\nAttempt:\n{self.difficulty}\n\n")
        #
        #         self.puzzle = deepcopy(puzzle1)
        #         if not self.check():
        #             puzzle1 = deepcopy(puzzle2)
        #             self.puzzle = deepcopy(puzzle2)
        #             print("NOTTTT")
        #         break
        #
        #     else:
        #         puzzle1 = deepcopy(self.puzzle)
        #
        #     if self.changes == 0:
        #         ct += 1
        #         self.try_insert(2)
        #         print(self.puzzle)
        #         print("\n\nTry\n\n")
        #
        #     if ct > 2:
        #         ct = 0
        #
        #         self.puzzle = deepcopy(puzzle1)
        #
        #     self.difficulty += 1
        #     if sum(sum(self.puzzle)) == 405 and self.check():
        #         print("\n\nSuccess\n\n")
        #         break
        #
        # if not self.check():
        #     print(f"\n\nFalied\n\n")
        end = timer()

        return self.puzzle, self.difficulty, end - start


def main():
    a, d, time = solve(ss.interface().foundation()).ai()
    print(f"Puzzle:\n{np.array(ss.interface().foundation())}")
    print(f"Time consumed: {round(time, 5)}\nDifficulty: {d}\nSolver:\n{a}\n")
    # print(f"Solution:\n{np.array(ss.interface(solution=True).foundation())}")
    # solve(ss.interface().print_board(a.tolist()))


if "__main__" == __name__:
    main()
