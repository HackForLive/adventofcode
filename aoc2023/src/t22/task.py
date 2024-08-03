import os
from typing import Dict, List, Set, Tuple
from pydantic import BaseModel



class Point(BaseModel):
    """
    Represents point using cartesian coordinates of three-dimensional space
    """
    x: int
    y: int
    z: int

    def __repr__(self):
        return f"P({self.x}, {self.y}, {self.z})"

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.x == other.x and
            self.y == other.y and
            self.z == other.z
        )

class Brick(BaseModel):
    """
    Brick is object with start point and end point
    """
    start: Point
    end: Point

    def __hash__(self):
        return hash((self.start, self.end))

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.start == other.start and
            self.end == other.end
        )


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
    print(f"{len(snapshot_bricks) = }")

    fallen_bricks = fall_process(snapshot_bricks=snapshot_bricks)
    print(f"{len(fallen_bricks) = }")

    removable_br = get_removable_bricks(fallen_bricks=fallen_bricks)
    print(f"{len(removable_br) = }")
    return len(removable_br)

def solve_2(in_f: str):
    snapshot_bricks = parse(input_file=in_f)
    print(f"{validate_input(bricks=snapshot_bricks) = }")
    print(f"{len(snapshot_bricks) = }")

    fallen_bricks = fall_process(snapshot_bricks=snapshot_bricks)
    print(f"{len(fallen_bricks) = }")

    brick_scores = get_brick_scores(fallen_bricks=fallen_bricks)
    # print(f"{brick_scores = }")
    # res = 0
    # for v, i in brick_scores.items():
    #     if not i:
    #         res += 1
    # print(f"{res =}")

    n = get_number_of_fallen_bricks(brick_scores=brick_scores, bricks=fallen_bricks)

    # print(f"{brick_scores = }")
    print(n)
    return n


def get_number_of_fallen_bricks(bricks: List[Brick], brick_scores: Dict[Brick, List[Brick]]):
    # could be optimized
    childs = {b: set() for b in bricks}
    for a in bricks:
        for b in bricks:
            if b.end.z + 1 == a.start.z and has_collision_in_xy(a=a, b=b):
                childs[a].add(b)

    # print(childs)
    res = 0
    for s in bricks:
        t_f = set(brick_scores[s])
        # print(t_f)
        # t_f.add(el_s)
        if not t_f:
            # empty
            continue

        for v in sorted(bricks, key=lambda x: x.start.z):
            if v == s:
                continue
            if not childs[v]:
                continue
            if childs[v].issubset(t_f):
                # fall
                if v not in t_f:
                    t_f.add(v)

        res += len(t_f)
    return res

def has_collision_in_xy(a: Brick, b: Brick) -> bool:

    if a.start.x > b.end.x:
        return False
    if a.end.x < b.start.x:
        return False
    if a.start.y > b.end.y:
        return False
    if a.end.y < b.start.y:
        return False

    return True

def get_removable_bricks(fallen_bricks: List[Brick]) -> List[Brick]:
    # from top to down
    res: List[Brick] = []

    s_fallen_bricks = sorted(fallen_bricks, key=lambda x: x.start.z)

    for b in s_fallen_bricks:
        # could be removed
        is_removable = True
        # check upper bricks
        for c in s_fallen_bricks:
            if c.start.z == b.end.z + 1 and has_collision_in_xy(a=c, b=b):
                is_removable = False
                for supp in s_fallen_bricks:
                    if supp in (b, c):
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


def get_brick_scores(fallen_bricks: List[Brick]) -> Dict[Brick, List[Brick]]:
    # from top to down
    s_fallen_bricks = sorted(fallen_bricks, key=lambda x: x.start.z)

    scores = {i: [] for i in fallen_bricks}

    for b in fallen_bricks:
        # could be removed
        is_removable = True
        # check upper bricks
        for c in fallen_bricks:
            if c.start.z == b.end.z + 1 and has_collision_in_xy(a=c, b=b):
                is_removable = False
                for supp in fallen_bricks:
                    if supp in (b, c):
                        continue
                    if supp.end.z == b.end.z and has_collision_in_xy(a=supp, b=c):
                        is_removable = True
                        break

                if not is_removable:
                    ## add
                    scores[b].append(c)
                    # break
            # if c.start.z > b.end.z + 1:
            #     break

    return scores


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
        for f in sorted(fallen_bricks, key=lambda l: l.end.z, reverse=True):
            # print(f)
            if has_collision_in_xy(a=f, b=brick):
                # print(f)
                # print(brick)
                fallen_bricks.append(Brick(
                    start=Point(x=brick.start.x, y=brick.start.y, z=f.end.z + 1),
                    end=Point(x=brick.end.x, y=brick.end.y,
                              z=f.end.z + 1 + brick.end.z - brick.start.z)))
                # print(fallen_bricks[-1])
                is_free = False
                break
        if is_free:
            # no collision
            fallen_bricks.append(Brick(
                        start=Point(x=brick.start.x, y=brick.start.y, z=1),
                        end=Point(x=brick.end.x, y=brick.end.y,
                                  z=1 + brick.end.z - brick.start.z)))

    return fallen_bricks


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
    test2_infile = os.path.join(curr_dir, 'test2.txt')
    infile = os.path.join(curr_dir, 'input.txt')

    check_collision_f()

    res_1 = solve_1(in_f=infile)

    # solve_1(in_f=test_infile)
    if res_1 == 416:
        print(f"Correct answer: {res_1}")
    else:
        print(f'Wrong answer: {res_1}, should be 416')

    res_2 = solve_2(in_f=infile)
    # 1207 ---> too low
    # 2472 ---> too low
    if res_2 == 60963:
        print(f"Correct answer: {res_2}")
    else:
        print(f'Wrong answer: {res_2}, should be: 60963')
