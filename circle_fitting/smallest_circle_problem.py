#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple


def _size(x):
    if isinstance(x, list):
        return len(x)
    elif isinstance(x, np.ndarray):
        return x.shape[0]
    else:
        return None

def _trivial_solve(R):
    if _size(R) == 0:
        return np.array([0, 0]), 0
    elif _size(R) == 1:
        return R[0], 0
    elif _size(R) == 2:
        c = (R[0] + R[1]) / 2.0
        d = R[0] - R[1]
        r = np.sqrt(d.dot(d)) / 2.0
        return c, r
    elif _size(R) == 3:
        c1, d1 = (R[0]+R[1])/2.0, R[0] - R[1]
        c2, d2 = (R[0]+R[2])/2.0, R[0] - R[2]
        g1 = -d1[0]/d1[1]
        g2 = -d2[0]/d2[1]
        cx = (np.dot([g1, -1], c1) - np.dot([g2, -1], c2)) / (g1 - g2)
        cy = g1*cx - np.dot([g1, -1], c1)
        c = np.array([cx, cy])
        d = R[0] - c
        r = np.sqrt(d.dot(d))

        for p1, p2, p3 in [(R[0], R[1], R[2]), (R[0], R[2], R[1]), (R[1], R[2], R[0])]:
            tc = (p1+p2) / 2.0
            td = p1 - p2
            tr = np.sqrt(td.dot(td)) / 2.0
            d3 = p3 - tc
            r3 = np.sqrt(d3.dot(d3))
            if r3 <= tr and tr < r:
                r = tr
                c = tc
        return c, r

def _welzl(P, R):
    if len(P) == 0 or len(R) >= 3:
        return _trivial_solve(R)
    else:
        c, r = _welzl(P[1:], R)
        d = P[0] - c
        l = np.sqrt(d.dot(d))
        if l <= r:
            return c, r
        return _welzl(P[1:], R + [P[0]])

def smallest_circle(points):
    '''https://en.wikipedia.org/wiki/Smallest-circle_problem
    '''
    idx = np.arange(0, len(points))
    np.random.shuffle(idx)
    return _welzl(points[idx], [])

if __name__ == '__main__':
    points = np.random.random((100, 2)) * 10.0
    print(points)
    c, r = smallest_circle(points)
    print(c, r)
    # c, r = _trivial_solve(points)
    # print(c, r)

    plt.plot(points[:, 0], points[:, 1], '^')
    theta = np.linspace(0, 2*np.pi, 100)
    x = c[0] + np.sin(theta) * r
    y = c[1] + np.cos(theta) * r
    plt.plot(x, y, '.')
    plt.show()
