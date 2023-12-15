from __future__ import annotations
import os
import pathlib
from typing import List


curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


def parse() -> List[str]:
    with open(input_file, 'r', encoding='utf8') as f:
        return f.readlines()[0].strip().split(',')

def get_hash_code(record: str) -> int:
    r_hash = 0
    for c in record:
        r_hash = ((r_hash + ord(c))*17)%256
    return r_hash

def solve_1():
    records = parse()
    res = sum((get_hash_code(record=record) for record in records))
    print(res)


if __name__ == '__main__':
    solve_1()
