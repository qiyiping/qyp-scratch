from __future__ import print_function
import copy

class ThreePigs(object):
    def __init__(self):
        self.templates = [
            [ [[-1,0],[0,1]], [[0,-1],[1,0]], [[1,0],[0,-1]], [[0,1],[-1,0]] ],
            [ [[0,1,0]], [[0],[1],[0]] ],
            [ [[-1,-1,0],[0,0,1]], [[0,-1],[0,-1],[1,0]], [[1,0,0],[0,-1,-1]], [[0,1], [-1,0], [-1, 0]]],
        ]
        self.arrangements = []
        self._cal_all_arrangements()

    def _cal_all_arrangements(self):
        b = [
            [-1,0,0,-1],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,-1]
        ]
        self._search(b, 0, [])

    def _search(self, b, step, trace):
        for p in self.templates[step]:
            matches = self._match(b, p)
            for m in matches:
                new_b = self._apply(b, p, m)
                new_trace = trace.copy()
                new_trace.append((p,m))
                if step == 2:
                    self.arrangements.append((new_trace, new_b))
                else:
                    self._search(new_b, step+1, new_trace)

    def _apply(self, b, p, m):
        h = len(p)
        w = len(p[0])
        i,j = m
        new_b = copy.deepcopy(b)
        for di in range(h):
            for dj in range(w):
                if p[di][dj] == 0:
                    new_b[i+di][j+dj] = 1
                if p[di][dj] == 1:
                    new_b[i+di][j+dj] = 2
        return new_b

    def _match(self, b, p):
        matches = []
        h = len(p)
        w = len(p[0])
        for i in range(4-h+1):
            for j in range(4-w+1):
                matched = True
                for di in range(h):
                    for dj in range(w):
                        if p[di][dj] != -1 and b[i+di][j+dj] != 0:
                            matched = False
                if matched:
                    matches.append((i,j))
        return matches

