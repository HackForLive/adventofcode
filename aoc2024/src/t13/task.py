import functools
from pathlib import Path
import re
from typing import List, Tuple

from attr import dataclass

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

@dataclass(frozen=True, init=True)
class Task:
    button_a: Tuple[int, int]
    button_b: Tuple[int, int]
    price: Tuple[int, int]

# linear equations
def get_price(
        a_cost: int,
        b_cost: int,
        task: Task) -> int:
    c1 = task.price[1]
    c2 = task.price[0]
    x1 = task.button_a[1]
    x2 = task.button_b[1]
    y1 = task.button_a[0]
    y2 = task.button_b[0]

    bn = c2*x1 - (y1*c1)
    bd = y2*x1 - (x2*y1)
    if bd == 0 or (bn % bd != 0):
        return 0
    else:
        b = bn // bd
    an = c1 - b*x2
    ad = x1
    if ad == 0 or (an % ad != 0):
        return 0
    else:
        a = an // ad

    if (a >= 0) and (b >= 0):
        return a_cost*a + b_cost*b
    return 0
    

def get_the_best_price(a_cost: int, b_cost: int, tasks: List[Task]) -> int:
    return functools.reduce(
            lambda a, b: a + b, [get_price(a_cost=a_cost, b_cost=b_cost, task=t) for t in tasks], 0)

# def prime_factors(n):
#     i = 2
#     factors = []
#     while i * i <= n:
#         if n % i:
#             i += 1
#         else:
#             n //= i
#             factors.append(i)
#     if n > 1:
#         factors.append(n)
#     return factors

@timer_decorator
def solve(p: Path, offset: int) -> int:
    a_cost = 3
    b_cost = 1
    tasks: List[Task] = []
    with open(p, encoding='utf-8', mode='r') as f:
        a = (-1, -1)
        b = (-1, -1)
        price = (-1, -1)
        for line in f:
            if line.startswith('Button A:'):
                matches = re.findall('X\\+(\\d+).*Y\\+(\\d+)', line)
                a = (int(matches[0][1]), int(matches[0][0]))
            elif line.startswith('Button B:'):
                matches = re.findall('X\\+(\\d+).*Y\\+(\\d+)', line)
                b = (int(matches[0][1]), int(matches[0][0]))
            elif line.startswith('Prize:'):
                matches = re.findall('X=(\\d+).*Y=(\\d+)', line)
                price = (int(matches[0][1]) + offset, 
                         int(matches[0][0]) + offset)
            else:
                tasks.append(Task(button_a=a, button_b=b, price=price))
                continue
        tasks.append(Task(button_a=a, button_b=b, price=price))
    return get_the_best_price(a_cost=a_cost, b_cost=b_cost, tasks=tasks)

if __name__ == '__main__':
    assert solve(p=t_f, offset=0) == 480
    assert solve(p=in_f, offset=0) == 28887
    assert solve(p=in_f, offset=10000000000000) == 96979582619758
    print("All passed!")
