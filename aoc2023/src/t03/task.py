from dataclasses import dataclass
import functools
import os
import pathlib
from typing import List, Tuple

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


@dataclass
class IndexPosition:
    start: int
    stop: int

@dataclass
class Position:
    index: IndexPosition
    row_id: int


def create_number_position(row_id: int, cfg: List[Tuple[int, int]]) -> Tuple[Position, int]:
    if cfg is None:
        raise ValueError('Number must exist')

    start = cfg[0][0]
    stop = cfg[-1][0]

    res = functools.reduce(lambda total, d: 10 * total + d, [f[1] for f in cfg], 0)


    return Position(row_id=row_id, index=IndexPosition(start=start, stop=stop)), res


# @timer_decorator
def solve_1():
    with open(input_file, 'r', encoding='utf8') as f:
        res = []
        symbols: List[Tuple[Position, str]] = []
        numb: List[Tuple[Position, int]] = []

        lines = f.readlines()

        for idx, line in enumerate(lines):
            l = line.strip()

            n: List[Tuple[int, int]] = []
            for idj, c in enumerate(l):
                if c == '.':
                    if n:
                        numb.append(create_number_position(row_id=idx, cfg=n))
                        n = []
                    continue
                # number
                if c.isdigit():
                    n.append((idj, int(c)))
                    if idj == len(l) - 1:
                        numb.append(create_number_position(row_id=idx, cfg=n))
                        n = []
                # symbol
                else:
                    if n:
                        # could be improved
                        numb.append(create_number_position(row_id=idx, cfg=n))
                        n = []
                    symbols.append((Position(row_id=idx, index=IndexPosition(start=idj, stop=idj)),
                                    c))

        for n in numb:
            y = n[0].row_id
            xsta = n[0].index.start
            xsto = n[0].index.stop
            for s in symbols:
                sy = s[0].row_id
                # same as stop
                sx= s[0].index.start
                if abs(y - sy) <= 1 and (xsta <= sx + 1 and xsto >= sx - 1):
                    res.append(n[1])

        print(sum(res))


# @timer_decorator
def solve_2():
    with open(input_file, 'r', encoding='utf8') as f:
        res = []
        symbols: List[Tuple[Position, str]] = []
        numb: List[Tuple[Position, int]] = []

        lines = f.readlines()

        for idx, line in enumerate(lines):
            l = line.strip()

            n: List[Tuple[int, int]] = []
            for idj, c in enumerate(l):
                if c == '.':
                    if n:
                        numb.append(create_number_position(row_id=idx, cfg=n))
                        n = []
                    continue
                # number
                if c.isdigit():
                    n.append((idj, int(c)))
                    if idj == len(l) - 1:
                        numb.append(create_number_position(row_id=idx, cfg=n))
                        n = []
                # symbol
                else:
                    if n:
                        # could be improved
                        numb.append(create_number_position(row_id=idx, cfg=n))
                        n = []
                    symbols.append((Position(row_id=idx, index=IndexPosition(start=idj, stop=idj)),
                                    c))


        for s in symbols:
            # gear
            if s[1] != '*':
                continue
            sy = s[0].row_id
            # same as stop
            sx= s[0].index.start

            res_tmp = []
            for n in numb:
                y = n[0].row_id
                xsta = n[0].index.start
                xsto = n[0].index.stop

                if abs(y - sy) <= 1 and (xsta <= sx + 1 and xsto >= sx - 1):
                    res_tmp.append(n[1])
            if len(res_tmp) == 2:
                res.append(np.prod(res_tmp))


        print(sum(res))


if __name__ == '__main__':
    solve_1()
    solve_2()
