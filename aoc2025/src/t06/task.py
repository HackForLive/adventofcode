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

@timer_decorator
def solve_2(p: Path):
    nums = []
    ops = []
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            line = l
            if not line:
                continue

            if '*' in line or '+' in line:
                ops = [i.strip() for i in line.split(' ') if i.strip()]
            else:
                nums.append(line)
    # print(nums)
    transposed = [''.join(col) for col in zip(*nums)]

    res = []
    tmp = []
    for i in transposed:
        curr = i.strip()
        if not curr:
            res.append(tmp)
            tmp = []
        else:
            tmp.append(int(curr))

    return compute(nums=res, ops=ops)

if __name__ == '__main__':
    assert solve_1(p=t_f) == 4277556
    print(solve_1(p=in_f)) # 4412382293768

    assert solve_2(p=t_f) == 3263827
    print(solve_2(p=in_f)) # 7858808482092
    print("All passed!")
