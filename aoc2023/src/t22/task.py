import os
from typing import List
from pydantic import BaseModel



class Point(BaseModel):
    """
    Represents point using cartesian coordinates of three-dimensional space
    """
    x: int
    y: int
    z: int

class Brick(BaseModel):
    """
    Brick is object with start point and end point
    """
    start: Point
    end: Point


def parse(input_file: str) -> List[Brick]:

    def get_brick_from_line(line: str, p_sep: str, c_sep: str) -> Brick:
        start, end = line.split(sep=p_sep)
        x, y, z = start.split(c_sep)
        s = Point(x=int(x), y=int(y), z=int(z))
        x, y, z = end.split(c_sep)
        e = Point(x=int(x), y=int(y), z=int(z))
        return Brick(start=s, end=e)

    with open(input_file, 'r', encoding='utf8') as f:
        bricks = [get_brick_from_line(line=line.strip(), p_sep='~', c_sep=',')
                  for line in f.readlines()]
    return bricks


def validate_input(bricks: List[Brick]) -> bool:
    res = True
    for b in bricks:
        res &= (b.start.x <= b.end.x) and (b.start.y <= b.end.y) and (b.start.z <= b.end.z)
    return res

def solve_1(in_f: str):
    snapshot_bricks = parse(input_file=in_f)
    print(f"{validate_input(bricks=snapshot_bricks) = }")
    print(snapshot_bricks)
    print(f"{len(snapshot_bricks) = }")

    fallen_bricks = fall_process(snapshot_bricks=snapshot_bricks)
    print(fallen_bricks)
    print(f"{len(fallen_bricks) = }")

    removable_br = get_removable_bricks(fallen_bricks=fallen_bricks)
    print(removable_br)
    print(f"{len(removable_br) = }")
    # too high - 1011, 907, 661


def has_collision_in_xy(a: Brick, b: Brick) -> bool:
    if a.start.x == a.end.x:
        # ax, bx constant
        if b.start.x == b.end.x:
            return (a.start.x == b.start.x) and (
                (b.start.y <= a.start.y <= b.end.y) or (b.start.y <= a.end.y <= b.end.y))
        # ax, by constant
        # ax, ay1 - ay2
        # bx1 - bx2, by
        return (a.start.y <= b.start.y <= a.end.y) and (b.start.x <= a.start.x <= b.end.x) 

    # ay, bx constant
    if b.start.x == b.end.x:
        # ax1 - ax2, ay
        # bx, by1 - by2
        return (a.start.x <= b.start.x <= a.end.x) and (b.start.y <= a.start.y <= b.end.y)
    # ay, by constant
    return (a.start.y == b.start.y) and (
        (b.start.x <= a.start.x <= b.end.x) or (b.start.x <= a.end.x <= b.end.x))

def get_removable_bricks(fallen_bricks: List[Brick]) -> List[Brick]:
    # from top to down
    res: List[Brick] = []
    for i, fb in zip(range(len(fallen_bricks)-1, -1, -1), reversed(fallen_bricks)):
        is_removable = True
        for r in reversed(res):
            if r.start.z - 1 == fb.end.z:
                if has_collision_in_xy(a=fb, b=r):
                    # check if it is support by other brick
                    is_removable = False
                    # TODO: optimize!
                    j = len(fallen_bricks)
                    while j >= 0:
                        j = j-1
                        if j == i:
                            continue
                        if fallen_bricks[j].end.z == fb.end.z:
                            if has_collision_in_xy(a=fallen_bricks[j], b=r):
                                is_removable = True
                                break
                            continue
                         # TODO: optimize!
                        if fallen_bricks[j].end.z >= fb.end.z:
                            continue
                        break
                    if is_removable:
                        break

            if r.start.z - 1 > fb.end.z:
                continue

        if is_removable:
            res.append(fb)
    return res


def fall_process(snapshot_bricks: List[Brick]) -> List[Brick]:
    # fall one by one sorted by start Z coordination
    sp_sorted = sorted(snapshot_bricks, key=lambda x: x.start.z)

    # keep already fallen bricks
    fallen_bricks: List[Brick] = []

    for brick in sp_sorted:
        # already fallen
        if brick.start.z == 1:
            fallen_bricks.append(brick)
            continue

        is_free = True
        # naively check all already fallen bricks
        # reversed return iterator, does not copy!
        for f in reversed(fallen_bricks):
            if has_collision_in_xy(a=f, b=brick):
                fallen_bricks.append(Brick(
                    start=Point(x=brick.start.x, y=brick.start.y, z=f.end.z + 1),
                    end=Point(x=brick.end.x, y=brick.end.y,
                              z=f.end.z + 1 + brick.end.z - brick.start.z)))
                is_free = False
                break

        if is_free:
            # no collision
            fallen_bricks.append(Brick(
                        start=Point(x=brick.start.x, y=brick.start.y, z=1),
                        end=Point(x=brick.end.x, y=brick.end.y,
                                  z=1 + brick.end.z - brick.start.z)))

    return fallen_bricks


def solve_2(in_f: str):
    points = parse(input_file=in_f)
    print(f"{len(points) = }")
    print(points)

if __name__ == '__main__':
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    test_infile = os.path.join(curr_dir, 'test.txt')
    infile = os.path.join(curr_dir, 'input.txt')

    solve_1(in_f=test_infile)
    # res_1 = solve_1(in_f=infile)
    # if res_1 == 3820:
    #     print(f"Correct answer: {res_1}, steps: {n}")
    # else:
    #     print(f'Wrong answer: {res_1}, steps: {n}')

    # res_2 = solve_2(in_f=test_infile)
    # if res_2 == 632421652138917:
    #     print(f"Correct answer: {res_2}, steps: {n}")
    # else:
    #     print(f'Wrong answer: {res_2}, steps: {n}')
