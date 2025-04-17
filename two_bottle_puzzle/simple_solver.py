from typing import List, Optional

def solve(m: int, n: int, k: int) -> Optional[List[str]]:
    if k > max(m, n):
        return None
    stat = [((0,0), ["Initial Stat: (0,0)"])]
    visited = set()
    while len(stat) > 0:
        s, trace = stat.pop()
        if s in visited:
            continue
        visited.add(s)
        if k in s:
            return trace
        new_s = (s[0], 0)
        stat.append((new_s, trace + [f"Empty 2: {new_s}"]))
        new_s = (0, s[1])
        stat.append((new_s, trace + [f"Empty 1: {new_s}"]))
        new_s = (s[0], n)
        stat.append((new_s, trace + [f"Fill 2: {new_s}"]))
        new_s = (m, s[1])
        stat.append((new_s, trace + [f"Fill 1: {new_s}"]))
        v = min(s[0], n-s[1])
        new_s = (s[0]-v, s[1]+v)
        stat.append((new_s, trace + [f"Move {v} from 1 to 2: {new_s}"]))
        v = min(s[1], m-s[0])
        new_s = (s[0]+v, s[1]-v)
        stat.append((new_s, trace + [f"Move {v} from 2 to 1: {new_s}"]))
    return None


if __name__ == '__main__':
    while True:
        x = input("problem > ")
        if x == 'quit':
            break
        m, n, k = [int(i) for i in x.split(' ')]
        r = solve(m, n, k)
        print("-" * 10)
        if r is None:
            print("It is infeasible.")
        else:
            print("It's feasible. The solution is:")
            print("\n".join(r))
