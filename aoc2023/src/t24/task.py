from dataclasses import dataclass
import pathlib

# 19, 13, 30 @ -2,  1, -2
# 18, 19, 22 @ -1, -1, -2
# 20, 25, 34 @ -2, -2, -4
# 12, 31, 28 @ -1, -2, -1
# 20, 19, 15 @  1, -5, -3

# px py pz @ vx vy vz
# moves in nano secs

@dataclass(frozen=True, init=True)
class Point2D():
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int


def parse(in_file: pathlib.Path) -> list[Point2D]:
    points = []
    with open(in_file, mode='r', encoding='utf-8') as f:
        for l in f:
            p, v = [[int(k) for k in i.split(',')] for i in l.split('@')]
            points.append(Point2D(x=p[0], y=p[1], z=p[2], vx=v[0], vy=v[1], vz=v[2]))
    return points

def is_valid_intersections(a: Point2D, b: Point2D, min_lim: int, max_lim: int) -> bool:
    # (x,y) = (ax, ay) + t*(avx, avy)
    # (x,y) = (bx, by) + k*(bvx, bvy) 
    # (bx, by) + k*(bvx, bvy) = (ax, ay) + t*(avx, avy)
    
    # k*bvx - t*avx = ax - bx ==> k = (ax - bx + t*avx) / bvx
    # k*bvy - t*avy = ay - by ==> bvy * (ax - bx + t*avx) / bvx - t*avy = ay - by

    # bvy * (ax - bx + t*avx) / bvx - t*avy = ay - by
    # t = [(ay - by) - bvy * (ax - bx) / bvx] / (bvy* avx / bvx - avy)
    t = 0
    k = 0

    if b.vx == 0:
        if a.vx == 0:
            return False
        else:
            t = (b.x - a.x) / a.vx
            x = a.x + t*a.vx
            y = a.y + t*a.vy
            k = (y - b.y) / b.vy 

    # cross product
    elif b.vy * a.vx - a.vy * b.vx == 0:
        return False
        
    else:
        t = ((a.y - b.y) - b.vy * (a.x - b.x) / b.vx) / (b.vy * a.vx / b.vx - a.vy)  
        x = a.x + t*a.vx
        y = a.y + t*a.vy
        k = (x - b.x) / b.vx 
        

    # back in time
    if t < 0 or k < 0:
        return False

    if x < min_lim or max_lim < x:
        return False
    
    if y < min_lim or max_lim < y:
        return False

    # print(x, y)
    return True


def get_valid_intersections(points: list[Point2D], min_lim: int, max_lim: int) -> int:
    res = 0
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            if is_valid_intersections(a=points[i], b=points[j], min_lim=min_lim, max_lim=max_lim):
                res += 1
    # print(res)
    return res


def solve(in_file: pathlib.Path, min_lim: int, max_lim: int) -> int:

    points = parse(in_file=in_file)
    
    return get_valid_intersections(points=points, min_lim=min_lim, max_lim=max_lim)

if __name__ == '__main__':
    curr_dir = pathlib.Path(__file__).parent
    input_file = curr_dir / 'test.txt'
    test_file = curr_dir / 'input_test.txt'

    assert solve(
        in_file=test_file, 
        min_lim=7,
        max_lim=27) == 2

    assert solve(
        in_file=input_file, 
        min_lim=200000000000000,
        max_lim=400000000000000) == 16018

