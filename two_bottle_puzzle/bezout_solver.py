#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from typing import Tuple, Optional, List


def extended_gcd(a:int, b:int) -> Tuple[int, int, int]:
    if b > a:
        g, x, y = extended_gcd(b, a)
        return g, y, x
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = extended_gcd(b, a % b)
        # g = x*b +y*(a - a//b * b) = y*a + x*b-y*(a//b)*b = y*a + (x-y*a//b)*b
        return g, y, x-y*(a//b)


def solve(m:int, n:int, k:int) -> Tuple[bool, Optional[List[str]]]:
    g, x, y = extended_gcd(m, n)
    if k % g != 0 or k > max(m, n):
        return False, None
    else:
        # return True, _build_actions(m, n, k, g, x, y)
        return True, None

def _build_actions(m, n, k, g, x, y) -> List[str]:
    t = k//g
    v = [m, n]
    p = [x*t, y*t]
    s = [0, 0]
    actions = []
    print(p, v)
    while p[0] != 0 or p[1] != 0 or k not in s:
        # fill
        fill_index = -1
        if p[0] > 0 and s[0] == 0:
            fill_index = 0
        elif p[1] > 0 and s[1] == 0:
            fill_index = 1
        if fill_index >= 0:
            prev_s = s[:]
            s[fill_index] = v[fill_index]
            p[fill_index] -= 1
            actions.append(f"Action: Fill {fill_index}, Status: {prev_s} -> {s}")
            continue
        # empty
        empty_index = -1
        if p[0] < 0 and s[0] == v[0]:
            empty_index = 0
        elif p[1] < 0 and s[1] == v[1]:
            empty_index = 1
        if empty_index >= 0:
            prev_s = s[:]
            s[empty_index] = 0
            p[empty_index] += 1
            actions.append(f"Action: Empty {empty_index}, Status: {prev_s} -> {s}")
            continue
        # move
        from_index = -1
        to_index = -1
        if p[0] > 0 and s[0] > 0:
            from_index = 0
            to_index = 1
        elif p[1] > 0 and s[1] > 0:
            from_index = 1
            to_index = 0
        if from_index >=0 and to_index >= 0:
            move_vol = min(s[from_index], v[to_index]-s[to_index])
            prev_s = s[:]
            s[from_index] -= move_vol
            s[to_index] += move_vol
            actions.append(f"Action: Move {move_vol} from {from_index} to {to_index}, Status: {prev_s} -> {s}")

    # assert (k in s)
    return actions



if __name__ == '__main__':
    while True:
        x = input("problem > ")
        if x == 'quit':
            break
        m, n, k = [int(i) for i in x.split(' ')]
        r, _ = solve(m, n, k)
        print(r)

        import puzzle
        r2 = puzzle.solve(m,n,k, print_actions=True)
        print(r2)
