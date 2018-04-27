#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt


class TSPSolverBase(object):
    def __init__(self, points, distances=None):
        self.points = points
        sz, _ = points.shape
        if distances is None:
            distances = np.zeros((sz, sz))
            for i in range(0, sz):
                for j in range(i+1, sz):
                    d = np.linalg.norm(points[i]-points[j])
                    distances[i][j] = d
                    distances[j][i] = d

        self.distances = distances
        self.size = sz

    def plot(self, route=None, figure_id=None):
        if figure_id is not None:
            plt.figure(figure_id)
        else:
            plt.figure()

        plt.scatter(self.points[:,0], self.points[:, 1])
        if route is not None:
            for i in range(0, len(route)-1):
                p1 = self.points[route[i]]
                p2 = self.points[route[i+1]]
                plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'g-')

            p1 = self.points[route[-1]]
            p2 = self.points[route[0]]
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'g-')

            r = self.evaluate(route)
            plt.title("length: {}".format(r))

    def evaluate(self, route):
        r = 0
        for i in range(0, len(route)-1):
            r += self.distances[route[i]][route[i+1]]
        r += self.distances[route[-1]][route[0]]
        return r

    def solve(self, **kwargs):
        """Return a random feasible solution"""
        route = np.arange(self.size)
        np.random.shuffle(route)
        return route

class NearestNeighborSolver(TSPSolverBase):
    def __init__(self, points, distances=None):
        super(NearestNeighborSolver, self).__init__(points, distances)

    def solve(self, **kwargs):
        start = kwargs.get("start", 0)
        route = [ start ]
        while len(route) < self.size:
            current_idx = route[-1]
            next_idx = -1
            next_val = -1
            for i in range(0, self.size):
                if i not in route:
                    if next_idx < 0 or self.distances[current_idx][i] < next_val:
                        next_idx = i
                        next_val = self.distances[current_idx][i]
            route.append(next_idx)
        return route

class TwoOptSolver(TSPSolverBase):
    def __init__(self, points, distances=None):
        super(TwoOptSolver, self).__init__(points, distances)

    def solve(self, **kwargs):
        route = kwargs.get("route") if kwargs.get("route") is not None else super(TwoOptSolver, self).solve()
        max_iters = kwargs.get("max_iters", 3000)
        debug = kwargs.get("debug", False)
        local_opt = False
        iters = 0
        while not local_opt and iters < max_iters:
            local_opt = True
            iters += 1
            for b in range(0, self.size-1):
                for e in range(b+1, self.size):
                    if e-b+1 < self.size-1:
                        bb = b-1 if b-1>0 else self.size-1
                        ee = e+1 if e+1<self.size else 0
                        v0 = self.distances[route[bb]][route[b]] + self.distances[route[e]][route[ee]]
                        v1 = self.distances[route[bb]][route[e]] + self.distances[route[b]][route[ee]]
                        if v1 < v0:
                            route = self.swap_2opt(route, b, e)
                            local_opt = False
                            break
                if not local_opt:
                    break

            # plot debug info
            if debug and iters % 10 == 0:
                self.plot(route, "debug")
                plt.pause(0.01)
                plt.gcf().clear()

        if debug:
            self.plot(route, "debug")
            plt.pause(0.01)
            print("number of iterations: {}".format(iters))

        return route

    def swap_2opt(self, route, b, e):
        new_route = []
        new_route.extend(route[:b])
        new_route.extend(reversed(route[b:e+1]))
        new_route.extend(route[e+1:])
        return new_route


if __name__ == '__main__':
    import time
    class Timing(object):
        def __init__(self):
            self.ts = time.time()

        def tell(self):
            return time.time() - self.ts

        def reset(self):
            self.ts = time.time()

        def tell_and_reset(self):
            now = time.time()
            t = now - self.ts
            self.ts = now
            return t



    num_of_points = 200
    points = np.random.rand(num_of_points, 2) * 10

    nn_solver = NearestNeighborSolver(points)
    timing = Timing()
    nn_solution = nn_solver.solve(start=2)
    print("nn solver: {}".format(timing.tell_and_reset()))
    nn_solver.plot(nn_solution)

    two_opt_solver = TwoOptSolver(points)
    timing.reset()
    two_opt_solution = two_opt_solver.solve(route=nn_solution, max_iters=1000, debug=True)
    print("2-opt solver: {}".format(timing.tell_and_reset()))

    plt.show()
