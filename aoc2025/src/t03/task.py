import functools
from pathlib import Path

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

def get_largest_number(bank: str, n: int) -> int:
    # n - length of number
    ll = len(bank)
    if ll < n:
        raise ValueError(f'n:{n} cannot be made from sequence with less length than n!')
    if ll == n:
        return int(bank)
    
    num = []
    start = 0

    for i in reversed(range(n)):
        top = bank[start]
        topi = start

        for k in range(start,ll-i):
            if top < bank[k]:
                top = bank[k]
                topi = k
        start = topi+1
        num.append(str(top))

    return int(''.join(num))



@timer_decorator
def solve_1(p: Path):
    with open(p, 'r', encoding='utf8') as f:
        return functools.reduce(
            lambda a, b: a + b, [get_largest_number(bank=l.strip(), n=2) for l in f])

@timer_decorator
def solve_2(p: Path):
    with open(p, 'r', encoding='utf8') as f:
        return functools.reduce(
            lambda a, b: a + b, [get_largest_number(bank=l.strip(), n=12) for l in f])

if __name__ == '__main__':
    assert solve_1(p=t_f) == 357
    print(solve_1(p=in_f)) # 17278
    
    assert solve_2(p=t_f) == 3121910778619
    print(solve_2(p=in_f)) # 171528556468625
    print("All passed!")
