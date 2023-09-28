# -*- coding: utf-8 -*-
import numpy as np
import itertools
from contextlib import contextmanager
from pprint import pprint


class Soduku(object):
    def __init__(self, problem):
        self.problem = problem

    def build_board(self):
        b = np.zeros((9,9), dtype=int)
        for r,c,v in self.problem:
            b[r-1, c-1] = v
        x, y = np.where(b==0)
        return b, list(zip(x,y))

    def solve(self):
        b, xy = self.build_board()
        s = np.zeros(len(xy), dtype=int)
        i = 0
        while True:
            if i < 0:
                return None
            if i >= len(xy):
                return b
            r, c = xy[i]
            br, bc = r//3, c//3
            l = np.zeros(10, dtype=int)
            for e in b[r, :]:
                l[e] = 1
            for e in b[:, c]:
                l[e] = 1
            for e in b[br*3: br*3+3, bc*3: bc*3+3].flatten():
                l[e] = 1
            s[i] += 1
            while s[i] <= 9 and l[s[i]] == 1:
                s[i] += 1
            if s[i] == 10:
                b[r, c] = 0
                s[i] = 0
                i -= 1
            else:
                b[r, c] = s[i]
                i += 1

if __name__ == '__main__':
    problem = [(1,1,8), (1,3,7), (1,4,5),
               (2,5,2), (2,9,3),
               (3,4,1), (3,6,4), (3,7,7),
               (4,1,3), (4,8,4), (4,9,6),
               (5,1,6), (5,3,2), (5,4,9), (5,6,1), (5,7,3), (5,9,5),
               (6,1,7), (6,2,1), (6,9,8),
               (7,3,3), (7,4,4), (7,6,8),
               (8,1,2), (8,5,9),
               (9,6,3), (9,7,5), (9,9,4)]
    soduku = Soduku(problem)
    b, _ = soduku.build_board()
    pprint(b)

    result = soduku.solve()
    if result is not None:
        pprint(result)
    else:
        print("NO SOLUTION FOUND.")
