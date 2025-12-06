import functools
from pathlib import Path

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

def compute(nums: list[list[int]], ops: list[str]):
    res = 0
    for idx, n in enumerate(nums):
        if ops[idx] == '+':
            r = functools.reduce(lambda x,y: x+y, n)
        elif ops[idx] == '*':
            r = functools.reduce(lambda x,y: x*y, n)
        else:
            raise ValueError('Incorrect op')
        res += r
    return res        


@timer_decorator
def solve_1(p: Path):
    nums = []
    ops = []
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            line = l.strip()
            if not line:
                continue

            ll = [i.strip() for i in line.split(' ') if i.strip()]

            if ll[0].isdigit():
                nums.append([int(i) for i in ll])
            else:
                ops=ll

    return compute(nums=list(map(list, zip(*nums))), ops=ops)

if __name__ == '__main__':
    assert solve_1(p=t_f) == 4277556
    print(solve_1(p=in_f)) # 520
    
    print("All passed!")
