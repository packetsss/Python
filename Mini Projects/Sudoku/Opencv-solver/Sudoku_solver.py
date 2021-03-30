"""
Stats:

    Method Average Time:
    init method: 0.0013
    unique method: 0.0076
    elimination method: 0.0038


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

Recursive implanted with Init, Unique and Elimination method:
Time consumed: 0.36783
Attempts: 32
"""

import numpy as np
from timeit import default_timer as timer
from copy import deepcopy


class solve:
    def __init__(self, p):
        self.puzzle, self.attempts, self.sets = np.array(p), 0, set(range(1, 10))

    @staticmethod
    def mini_nine(puzzle):
        return np.array([(np.reshape(puzzle[i:i + 3, j:j + 3], (1, 9))[0])
                         for i in range(0, 7, 3) for j in range(0, 7, 3)])

    @staticmethod
    def mn_index(i, j):
        return i // 3 * 3 + i // 3, (i % 3) * 3 + (j % 3)

    @staticmethod
    def mn_index_block(i, j):
        return int(i / 3) * 3, int(i / 3) * 3 + 3, int(j / 3) * 3, int(j / 3) * 3 + 3

    def init(self, p):
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
                        p[i, j] = int("".join(map(str, self.sets
                                                  .difference(set(row))
                                                  .difference(set(col))
                                                  .difference(set(mn_puz)))))
                    except ValueError:
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
    def unique_mod(p):
        for i in range(9):
            row = "".join(map(str, p[i, :]))
            col = "".join(map(str, p[:, i]))
            for num in range(1, 10):

                if row.count(str(num)) == 1:
                    for j in range(9):
                        if str(num) in str(p[i, j]):
                            try:
                                p[:, j] = [int(s.replace(str(num), '')) for s in list(map(str, p[:, j]))]
                            except ValueError:
                                pass
                            p[i, j] = num
                            break

                if col.count(str(num)) == 1:
                    for j in range(9):
                        if str(num) in str(p[j, i]):
                            try:
                                p[j, :] = [int(s.replace(str(num), '')) for s in list(map(str, p[j, :]))]
                            except ValueError:
                                pass
                            p[j, i] = num
                            break
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
                                print(f"Failed at elimination | i = {i} | j = {j}")
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
                                print(f"Failed at elimination | i = {i} | j = {j}")
                                return False
        return True

    # def try_insert(self, length=2):
    #     for i in range(9):
    #         for j in range(9):
    #             if len(str(self.puzzle[i, j])) == length:
    #                 self.puzzle[i, j] = random.choice([int(i) for i in str(self.puzzle[i, j])])
    #                 return None

    def check(self, p):
        for i in range(9):
            row = [i for i in p[i, :] if len(str(i)) == 1]
            if len(set(row)) != len(row):
                print(f"Failed at check: row {row}")
                return False

            col = [i for i in p[:, i] if len(str(i)) == 1]
            if len(set(col)) != len(col):
                print(f"Failed at check: col {col}")
                return False

            a1, a3, b1, b3 = self.mn_index_block(i, i % 3 * 3)
            mn_puz = np.reshape(self.puzzle[a1:a3, b1:b3], (1, 9))[0]
            mn_row = [i for i in mn_puz if len(str(i)) == 1]
            if len(set(mn_row)) != len(mn_row):
                print(f"Failed at check: mn_nine {mn_row}")
                return False
            return True

    def check_v2(self, i, j, k):

        if k in self.puzzle[i, :]:
            #print(f"Failed at check_v2: {self.puzzle[i, :]}")
            return False

        if k in self.puzzle[:, j]:
            #print(f"Failed at check_v2: {self.puzzle[:, j]}")
            return False

        a1, a3, b1, b3 = self.mn_index_block(i, j)
        mn_puz = np.reshape(self.puzzle[a1:a3, b1:b3], (1, 9))[0]
        if k in mn_puz:
            #print(f"Failed at check_v2: mn_nine")
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

    def try_insert(self):
        p = deepcopy(self.puzzle)

        try:
            i, j = self.out()
        except TypeError:
            if sum(sum(self.puzzle)) == 405:
                return True
            else:
                print(f"\n\nFailed at the FINAL STEP!! Grid:\n{self.puzzle}\n\n")
                return False

        for k in [int(k) for k in str(self.puzzle[i, j])]:
            print(f"Now inserting \"{k}\" | ({i}, {j})")
            self.puzzle[i, j] = k

            if not self.init(self.puzzle) or not self.unique(self.puzzle) \
                    or not self.elimination(self.puzzle) or not self.check(self.puzzle):
                self.puzzle = deepcopy(p)
                continue
            else:
                self.unique_mod(p)
                if self.try_insert():
                    return True
                else:

                    self.puzzle = deepcopy(p)
        print(f"Back Tracking... | i: {i} | j: {j}")
        self.attempts += 1
        return False

    def ai(self):
        start = timer()
        self.init(self.puzzle)
        print(self.puzzle)
        self.try_insert()

        if not self.check(self.puzzle) or sum(sum(self.puzzle)) != 405:
            print(f"\nSolving Failed!\n".upper())
            return False
        else:
            print("\nSolving Success!\n".upper())
        end = timer()
        return self.puzzle, self.attempts, end - start
