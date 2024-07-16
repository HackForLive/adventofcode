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

def solve_1(in_f: str):
    points = parse(input_file=in_f)
    print(points)

def solve_2(in_f: str):
    points = parse(input_file=in_f)
    print(points)

if __name__ == '__main__':
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    test_infile = os.path.join(curr_dir, 'test.txt')
    infile = os.path.join(curr_dir, 'input.txt')

    solve_1(in_f=infile)
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
