from dataclasses import dataclass
import os
import pathlib
from typing import Iterator, List
from line_profiler import LineProfiler

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int


@dataclass
class Instruction:
    axe: str
    n: int


def project_point_by_x(point: Point, mid: int) -> Point:
    if point.x > mid:
        if point.x - mid <= mid:
            return Point(x=mid - (point.x - mid), y = point.y)
        else:
            return None
    else:
        return point


def project_point_by_y(point: Point, mid: int) -> Point:
    if point.y > mid:
        if point.y - mid <= mid:
            return Point(x=point.x, y = mid - (point.y - mid))
        else:
            return None
    else:
        return point


def project_points(points: List[Point], instruction: Instruction) -> Iterator[Point]:
    # print(f"{instruction.axe =}, {instruction.n}")
    for point in points:
        if instruction.axe == 'x':
            yield project_point_by_x(point=point, mid = instruction.n)
        elif instruction.axe == 'y':
            yield project_point_by_y(point=point, mid = instruction.n)
        else:
            raise NotImplementedError('No such axis supported!')


def loop_over_instructions(points: List[Point], instructions: List[Instruction]) -> Iterator[Point]:
    curr = points
    for instr in instructions:
        curr = project_points(points=curr, instruction=instr)
    return curr


def solve_1():
    with open(input_file, 'r', encoding='utf8') as f:
        n_list: List[Point] = []
        instr: List[Instruction] = []
        for line in f:
            curr = line.strip()
            if ',' in curr:
                parts = curr.split(',')
                n_list.append(Point(int(parts[0]), int(parts[1])))
            elif '=' in curr:
                parts = curr.split(' ')[2].split('=')
                instr.append(Instruction(axe=parts[0], n=int(parts[1])))

        res = set(loop_over_instructions(points=n_list, instructions=[instr[0]]))
        # print(res)
        print(len(res))


def solve_2():
    with open(input_file, 'r', encoding='utf8') as f:
        n_list: List[Point] = []
        instr: List[Instruction] = []
        for line in f:
            curr = line.strip()
            if ',' in curr:
                parts = curr.split(',')
                n_list.append(Point(int(parts[0]), int(parts[1])))
            elif '=' in curr:
                parts = curr.split(' ')[2].split('=')
                instr.append(Instruction(axe=parts[0], n=int(parts[1])))

        res = set(loop_over_instructions(points=n_list, instructions=instr))

        x_min = min((item.n for item in instr if item.axe == 'x'))
        y_min = min((item.n for item in instr if item.axe == 'y'))

        m = np.zeros([y_min, x_min], dtype=int)
        # for y, x in np.ndindex(m.shape):
        for item in res:
            if item:
                m[item.y, item.x] = 1
        with open(os.path.join(curr_dir, 'outfile.txt'), mode='w', encoding='utf-8') as f:
            np.savetxt(f, m, fmt='%.0f', delimiter=',')


if __name__ == '__main__':
    # solve_1()
    # solve_2()
    lp = LineProfiler()
    lp.add_function(project_points)
    lp.add_function(loop_over_instructions)
    # lp_wrapper = lp(solve_1)
    lp_wrapper = lp(solve_2)
    lp_wrapper()
    lp.print_stats()
