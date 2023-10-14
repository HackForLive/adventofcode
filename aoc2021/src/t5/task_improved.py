import pathlib
import os
from typing import List

import numpy as np

class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    def __eq__(self, obj):
        return isinstance(obj, Point) and obj.x == self.x and obj.y == self.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
        

class Line:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'input.txt')

def parse_line_from_points(points_raw: List[str]) -> Line:
    if points_raw and len(points_raw) == 2:
        start_p_raw = points_raw[0].split(',')
        start = Point(x=int(start_p_raw[0]), y=int(start_p_raw[1]))
        end_p_raw = points_raw[1].split(',')
        end = Point(x=int(end_p_raw[0]), y=int(end_p_raw[1]))
        return Line(start=start, end=end)
    else:
        raise ValueError('Issue with parsing points into line.')
    
def get_intersection_points(a: Line, b: Line) -> List[Point]:
    # AB, nAB          an * x + bn * y   + c = 0
    # a1 b1 -c
    # a2 b2 -c

    return set(a_points).intersection(set(b_points))


def get_only_vertical_and_horizontal_lines(lines: List[Line]):
    return list(filter(lambda x: x.start.x == x.end.x or x.start.y == x.end.y, lines))

def get_only_vertical_and_horizontal_and_diag_lines(lines: List[Line]):
    return list(filter(lambda x:
                       x.start.x == x.end.x or
                       x.start.y == x.end.y or
                       abs(abs(x.start.y - x.end.y) - abs(x.start.x - x.end.x)) < 1e-9, lines))

# diag a,b ->  a + c, b - c
# diag a,b ->  a + c, b + c
# diag a,b ->  a - c, b - c
# diag a,b ->  a - c, b + c

def solve_1():
    with open(input_file, 'rt', encoding='utf8') as f:
        lines = [parse_line_from_points([points.strip() for points in line.strip().split('->')]) for line in f]
        lines = get_only_vertical_and_horizontal_lines(lines=lines)
        points = set()
        for i in range(0, len(lines)):
            for j in range(i+1, len(lines)):
                tmp = get_intersection_points(a=lines[i],b=lines[j])
                points.update(tmp)
    
    print(len(points))


def solve_2():
    with open(input_file, 'rt', encoding='utf8') as f:
        lines = [parse_line_from_points([points.strip() for points in line.strip().split('->')]) for line in f]
        lines = get_only_vertical_and_horizontal_and_diag_lines(lines=lines)
        points = set()
        for i in range(0, len(lines)):
            for j in range(i+1, len(lines)):
                tmp = get_intersection_points(a=lines[i],b=lines[j])
                points.update(tmp)
    
    print(len(points))


if __name__ == '__main__':
    # 8 seconds --> improve
    solve_1()
    solve_2()
