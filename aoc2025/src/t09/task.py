from pathlib import Path
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

Point = tuple[int,int]

def compute_max_area(pts: list[Point]):
    return max(((abs(s[0]-f[0])+1)*(abs(s[1]-f[1])+1) for f in pts for s in pts))


def area(a: Point, b: Point):
    return (abs(a[0]-b[0])+1)*(abs(a[1]-b[1])+1)



def is_valid(a: Point, b: Point, pts: list[Point]):
    # outside or intersect

    for i in range(0,len(pts)):
        d = pts[i]
        c = pts[i-1]
        # print(f"{(a[0], b[1]) =}, {b =}, {c =}, {d =}")
        
        if d[0] == c[0]:
            # x fixed
            if min(a[0],b[0]) < d[0] < max(a[0],b[0]):
                # print('here 1')
                # if not outside
                if  not (
               ( min(a[1], b[1]) >= max(c[1], d[1])) or (max(a[1], b[1]) <= min(c[1], d[1]))):
                    return False
        if d[1] == c[1]:
            # x
            if min(a[1],b[1]) < d[1] < max(a[1],b[1]):
                # if not outside
                # print('here 2')
                if not (
               ( min(a[0], b[0]) >= max(c[0], d[0])) or (max(a[0], b[0]) <= min(c[0], d[0]))):
                    return False
                                                          
    return True

def compute_max_area_with_restriction(pts: list[Point]):
    """
    Red points the opposite => inside only green/red
    
    :param pts: 2D points
    :type pts: list[tuple[int, int]]
    """

    # tests
    # print(is_valid(a=(9,7),b=(2,3),pts=pts))
    # print(is_valid(a=(9,5),b=(2,3),pts=pts))

    res = 0
    # check the rectangle
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            # print(f"{i =}, {j =}")
            if is_valid(a=pts[i], b=pts[j], pts=pts):
                tmp = area(a=pts[i], b=pts[j])
                if tmp > res:
                    res = tmp

    # max_x = 0
    # min_x = sys.maxsize

    # max_y = 0
    # min_y = sys.maxsize


    # for p in pts:
    #     if p[0] > max_x:
    #         max_x = p[0]
    #     if p[0] < min_x:
    #         min_x = p[0]

    #     if p[1] > max_y:
    #         max_y = p[1]
    #     if p[1] < min_y:
    #         min_y = p[1]

    # arr = np.zeros((max_y-min_y+1, max_x-min_x+1), dtype=int)

    # for c, r in pts:
    #     arr[r-min_y, c-min_x] = 1
    
    # np.savetxt("/home/malisha/git/adventofcode/aoc2025/src/t09/output.txt", arr, fmt='%d')
    print(res)
    return res

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
    print(solve_2(p=in_f)) # 1540192500
    print("All passed!")
