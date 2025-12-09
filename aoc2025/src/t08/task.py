import math
from pathlib import Path
import sys

from aoc.model.geometry import Point3D
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

def euc_dist(a: Point3D, b: Point3D):
    return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2 + (a.z-b.z)**2)

def compute(pts: list[Point3D], n: int | None):
    circuits = {}
    for p in pts:
        circuits[p] = set([p])

    dist_p ={}

    for fi, f in enumerate(pts):
        for si, s in enumerate(pts):
            if fi == si:
                continue
            if not (s.x, s.y, s.z)+ (f.x, f.y, f.z) in dist_p:
                dist_p[(f.x, f.y, f.z)+(s.x, s.y, s.z)] = euc_dist(f, s)

    closest_dists_s = dict(sorted(dist_p.items(), key=lambda item: item[1]))

    counter = 0
    res = 0
    for k,v in closest_dists_s.items():
        if n and not counter < n:
            break
        counter += 1
        
        fir = Point3D(x=k[0], y=k[1], z=k[2])
        sec = Point3D(x=k[3], y=k[4], z=k[5])

        if (sec not in circuits[fir]) and (fir not in circuits[sec]):
            uni = set(circuits[fir].union(circuits[sec]))
            for i in uni:
                circuits[i]=uni
            res = fir.x*sec.x
    if not n:
        return res
    
    largest_circuits = dict(sorted(circuits.items(), key=lambda item: len(item[1]), reverse=True))

    res = 1
    c = 0
    curr = None
    for k,v in largest_circuits.items():
        
        if not c < 3:
            break
        if curr == v:
            continue
        res *= len(v)
        c += 1
        curr = v
    return res

@timer_decorator
def solve_1(p: Path, n: int):
    points = []
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            x,y,z = [int(i) for i in l.strip().split(',')]
            points.append(Point3D(x=x,y=y,z=z))

    return compute(pts=points, n=n)

@timer_decorator
def solve_2(p: Path):
    points = []
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            x,y,z = [int(i) for i in l.strip().split(',')]
            points.append(Point3D(x=x,y=y,z=z))

    return compute(pts=points, n=None)

if __name__ == '__main__':
    assert solve_1(p=t_f, n=10) == 40
    print(solve_1(p=in_f, n=1000)) # 32103

    assert solve_2(p=t_f) == 25272
    print(solve_2(p=in_f)) # 8133642976
    print("All passed!")
