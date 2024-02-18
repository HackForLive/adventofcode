from __future__ import annotations
from ast import Tuple
from enum import Enum
import os
import pathlib
from typing import List, NamedTuple


curr_dir = pathlib.Path(__file__).parent.resolve()


class Direction(Enum):
    """
    U/D/L/R
    """
    U = [-1, 0]
    R = [0, 1]
    D = [1, 0]
    L = [0, -1]


def get_dir_by_num(n: int) -> Direction:
    if n == 0:
        return Direction.R
    if n == 1:
        return Direction.D
    if n == 2:
        return Direction.L
    if n == 3:
        return Direction.U
    raise ValueError("Unexpected mapping.")


class Point(NamedTuple):
    """
    Point
    """
    x: int
    y: int


def parse(in_file: str) -> Tuple[List[Point], int]:
    p = Point(x=0, y=0)
    c_points: List[Point] = []
    l = 0
    with open(in_file, 'r', encoding='utf8') as f:
        for line in f:
            direction, steps, _ = line.strip().split(' ')

            tmp_dir = Direction[direction].value

            l += int(steps)

            p = Point(x=p.x + tmp_dir[1], y=p.y + tmp_dir[0])
            c_points.append(Point(x=p.x, y=p.y))
            p = Point(x=p.x + (int(steps)-1)*tmp_dir[1], y=p.y + (int(steps)-1)*tmp_dir[0])
            c_points.append(Point(x=p.x, y=p.y))
    return c_points, l


def parse_2(in_file: str) -> Tuple[List[Point], int]:
    p = Point(x=0, y=0)
    c_points: List[Point] = []
    l = 0
    with open(in_file, 'r', encoding='utf8') as f:
        for line in f:
            _, steps, color = line.strip().split(' ')

            hex_code = color[2:-1]
            steps = int(hex_code[:-1], 16)
            direction = int(hex_code[-1])

            tmp_dir = get_dir_by_num(n=direction).value
            l += int(steps)

            p = Point(x=p.x + tmp_dir[1], y=p.y + tmp_dir[0])
            c_points.append(Point(x=p.x, y=p.y))
            p = Point(x=p.x + (int(steps)-1)*tmp_dir[1], y=p.y + (int(steps)-1)*tmp_dir[0])
            c_points.append(Point(x=p.x, y=p.y))
    return c_points, l


def points_inside(area: float, boarder_pts: int):
    return area - boarder_pts/2 + 1


def polygon_area(c_points: List[Point]):
    # Initialize area
    area = 0.0

    polygon_pts = [(m.y, m.x) for m in c_points]
    n = len(polygon_pts)

    # Calculate value of shoelace formula
    j = n - 1
    for i in range(0,n):
        area += (polygon_pts[j][1] + polygon_pts[i][1]) * (polygon_pts[j][0] - polygon_pts[i][0])
        j = i   # j is previous vertex to i

    # Return absolute value
    return int(abs(area / 2.0))


def solve_1():

    cases = ['input_1.txt', 'test.txt']
    expected = [62, 31171]
    for idx, case in enumerate(cases):
        input_file = os.path.join(curr_dir, case)
        c_points, border_pts_len = parse(in_file=input_file)
        area = polygon_area(c_points=c_points)
        i = points_inside(area=area, boarder_pts=border_pts_len)

        print(i+border_pts_len)
        assert int(i+border_pts_len) == expected[idx], 'Wrong answer'


def solve_2():

    cases = ['input_1.txt', 'test.txt']
    expected = [952408144115, 131431655002266]
    for idx, case in enumerate(cases):
        input_file = os.path.join(curr_dir, case)
        c_points, border_pts_len = parse_2(in_file=input_file)
        area = polygon_area(c_points=c_points)
        i = points_inside(area=area, boarder_pts=border_pts_len)
        print(i+border_pts_len)
        assert int(i+border_pts_len) == expected[idx], 'Wrong answer'


if __name__ == '__main__':
    solve_1()
    solve_2()
