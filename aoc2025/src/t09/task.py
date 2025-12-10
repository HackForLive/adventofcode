from pathlib import Path

from aoc.model.direction import Direction
from aoc.model.geometry import Point3D
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

def compute_max_area(pts: list[tuple[int,int]]):
    return max(((abs(s[0]-f[0])+1)*(abs(s[1]-f[1])+1) for f in pts for s in pts))

def next_dir(a: tuple[int, int], b: tuple[int, int]):
    if a[0] == b[0]:
        if a[1] == b[1]:
            raise ValueError() 
        return Direction.NORTH if a[1] > b[1] else Direction.SOUTH
    return Direction.EAST if a[0] < b[0] else Direction.WEST

def get_opposite(a: Direction):
    if a == Direction.NORTH: return Direction.SOUTH
    if a == Direction.SOUTH: return Direction.NORTH
    if a == Direction.EAST: return Direction.WEST
    if a == Direction.WEST: return Direction.EAST
    raise ValueError()

def convex_hull(points):
    points = sorted(set(points))

    if len(points) <= 1:
        return points

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - \
               (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


def compute_max_area_with_restriction(pts: list[tuple[int,int]]):
    """
    Red points the opposite => inside only green/red
    
    :param pts: 2D points
    :type pts: list[tuple[int, int]]
    """
    print(pts)
    
    hull = convex_hull(pts)
    print(hull)
    return 0

@timer_decorator
def solve_1(p: Path):
    points = []
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            x,y = [int(i) for i in l.strip().split(',')]
            points.append((x,y))

    return compute_max_area(pts=points)

@timer_decorator
def solve_2(p: Path):
    points = []
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            x,y = [int(i) for i in l.strip().split(',')]
            points.append((x,y))

    return compute_max_area_with_restriction(pts=points)

if __name__ == '__main__':
    assert solve_1(p=t_f) == 50
    print(solve_1(p=in_f)) # 4744899849

    assert solve_2(p=t_f) == 24
    # print(solve_2(p=in_f)) # 7858808482092
    print("All passed!")
