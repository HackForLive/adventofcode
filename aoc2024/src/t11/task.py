from pathlib import Path
from typing import List
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

dd = {}

def apply_action(blink: int, number: int) -> int:
    if blink == 0:
        return 1
    if (number, blink) in dd:
        return dd[(number, blink)]
    if number == 0:
        a = apply_action(blink=blink-1, number=1)
        dd[(number, blink)] = a
        return dd[(number, blink)]
    elif len(str(number)) % 2 == 0:
        n = len(str(number))
        l = apply_action(blink=blink-1, number=int(str(number)[:n//2]))
        r = apply_action(blink=blink-1, number=int(str(number)[n//2:]))
        dd[(number, blink)] = l + r
        return dd[(number, blink)]
    else:
        a = apply_action(blink=blink-1, number=number*2024)
        dd[(number, blink)] = a
        return a

def get_number_of_stones(blinks: int, numbers: List[int]) -> int:
    res = 0
    for n in numbers:
        res += apply_action(blink=blinks, number=n)
    return res

@timer_decorator
def solve(p: Path, blinks: int) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        for line in f:
            numbers = [int(i) for i in line.strip().split(' ') if i]
            return get_number_of_stones(blinks=blinks, numbers=numbers)
        return 0

if __name__ == '__main__':
    assert solve(p=t_f, blinks=25) == 55312
    assert solve(p=in_f, blinks=25) == 203228
    assert solve(p=in_f, blinks=75) == 240884656550923
    print("All passed!")
