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
        # res &= (b.start.x <= b.end.x) and (b.start.y <= b.end.y) and (b.start.z <= b.end.z)
        tmp = (
            ((b.start.x == b.end.x) and (b.start.y == b.end.y) and (b.start.z <= b.end.z)) or
            ((b.start.x <= b.end.x) and (b.start.y == b.end.y) and (b.start.z == b.end.z)) or
            ((b.start.x == b.end.x) and (b.start.y <= b.end.y) and (b.start.z == b.end.z))
        )
        if not tmp:
            print(b)
        res &= tmp
    return res

def solve_1(in_f: str) -> int:
    snapshot_bricks = parse(input_file=in_f)
    print(f"{validate_input(bricks=snapshot_bricks) = }")
    # print(snapshot_bricks)
    print(f"{len(snapshot_bricks) = }")

    fallen_bricks = fall_process(snapshot_bricks=snapshot_bricks)
    # print(fallen_bricks)
    print(f"{len(fallen_bricks) = }")

    removable_br = get_removable_bricks(fallen_bricks=fallen_bricks)
    # print(removable_br)
    print(f"{len(removable_br) = }")
    # too high - 1011, 907, 661
    # missed 476
    return len(removable_br)


def has_collision_in_xy(a: Brick, b: Brick) -> bool:
    if a.start.x == a.end.x:
        # ax, bx constant
        if b.start.x == b.end.x:
            return (a.start.x == b.start.x) and not ((b.start.y > a.end.y) or (a.start.y > b.end.y))
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
    return (a.start.y == b.start.y) and not ((b.start.x > a.end.x) or (a.start.x > b.end.x))

def get_removable_bricks(fallen_bricks: List[Brick]) -> List[Brick]:
    # from top to down
    res: List[Brick] = []

    s_fallen_bricks = sorted(fallen_bricks, key=lambda x: x.start.z)

    for i, b in enumerate(s_fallen_bricks):
        # could be removed
        is_removable = True
        # check upper bricks
        for j, c in enumerate(s_fallen_bricks):
            if c.start.z == b.end.z + 1 and has_collision_in_xy(a=c, b=b):
                is_removable = False
                for s, supp in enumerate(s_fallen_bricks):
                    if s in (j, i):
                        continue
                    if supp.end.z == b.end.z and has_collision_in_xy(a=supp, b=c):
                        is_removable = True
                        break

                if not is_removable:
                    break
            if c.start.z > b.end.z + 1:
                break
        if is_removable:
            res.append(b)

    return res


def fall_process(snapshot_bricks: List[Brick]) -> List[Brick]:
    # print(sp_sorted)
    # keep already fallen bricks
    fallen_bricks: List[Brick] = []

    # fall one by one sorted by start Z coordination
    for brick in sorted(snapshot_bricks, key=lambda x: x.start.z):
        # already fallen
        if brick.start.z == 1:
            fallen_bricks.append(brick)
            continue

        is_free = True
        # naively check all already fallen bricks
        # reversed return iterator, does not copy!
        for f in sorted(fallen_bricks, key=lambda x: x.end.z, reverse=True):
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

def check_collision_f() -> bool:
    tmp = has_collision_in_xy(
        a=Brick(start=Point(x=1,y=1,z=1), end=Point(x=1,y=1,z=1)),
        b=Brick(start=Point(x=1,y=1,z=1), end=Point(x=1,y=1,z=1)))
    assert tmp

    tmp = has_collision_in_xy(
        a=Brick(start=Point(x=1,y=1,z=1), end=Point(x=2,y=2,z=2)),
        b=Brick(start=Point(x=1,y=1,z=1), end=Point(x=1,y=1,z=1)))
    assert tmp

    tmp = has_collision_in_xy(
        a=Brick(start=Point(x=2,y=1,z=1), end=Point(x=2,y=2,z=2)),
        b=Brick(start=Point(x=1,y=1,z=1), end=Point(x=1,y=1,z=1)))
    assert not tmp

    tmp = has_collision_in_xy(
        a=Brick(start=Point(x=1,y=1,z=10), end=Point(x=1,y=1,z=10)),
        b=Brick(start=Point(x=1,y=0,z=1), end=Point(x=1,y=10,z=1)))
    assert tmp
    return True

if __name__ == '__main__':
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    test_infile = os.path.join(curr_dir, 'test.txt')
    infile = os.path.join(curr_dir, 'input.txt')

    check_collision_f()

    res_1 = solve_1(in_f=infile)

    # solve_1(in_f=test_infile)
    if res_1 == 416:
        print(f"Correct answer: {res_1}")
    else:
        print(f'Wrong answer: {res_1}')

    # res_2 = solve_2(in_f=test_infile)
    # if res_2 == 632421652138917:
    #     print(f"Correct answer: {res_2}, steps: {n}")
    # else:
    #     print(f'Wrong answer: {res_2}, steps: {n}')
