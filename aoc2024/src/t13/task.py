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

# greedy strategy
def get_price(
        max_blicks: int,
        a_cost: int,
        b_cost: int,
        task: Task) -> int:
    # assume a_cost lower than b_cost
    if a_cost < b_cost:
        raise NotImplementedError()
    
    min_price = None

    for a in range(0, max_blicks + 1):
        x = (task.price[0] - a*task.button_a[0], task.price[1] - a*task.button_a[1])
        
        if ((x[0] % task.button_b[0]) == 0) and ((x[1] % task.button_b[1]) == 0):
            b = x[0] // task.button_b[0]
            if b == (x[1] // task.button_b[1]):
                min_price = a_cost*a + b_cost*b
                break

    if not min_price:
        return 0
    return min_price

def get_the_best_price(a_cost: int, b_cost: int, tasks: List[Task]) -> int:
    res = 0
    for task in tasks:
        res += get_price(
            max_blicks=100,
            a_cost=a_cost,
            b_cost=b_cost,
            task=task)
    return res


def get_the_best_price_2(a_cost: int, b_cost: int, tasks: List[Task]) -> int:
    res = 0
    for t in tasks:
        min_price = None
        for a in range(0, 10000000000000000, 10000000000):
            
            x = (t.price[0] - a*t.button_a[0], t.price[1] - a*t.button_a[1])
            
            if ((x[0] % t.button_b[0]) == 0) and ((x[1] % t.button_b[1]) == 0):
                # found possible b!
                print(x[0] // t.button_b[0])
                print(x[1] // t.button_b[1])
                b = x[0] // t.button_b[0]
                if b == (x[1] // t.button_b[1]):
                    min_price = a_cost*a + b_cost*b
                    break

        if not min_price:
            min_price = 0
        res += min_price

    return res

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
def solve_1(p: Path) -> int:
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
                price = (int(matches[0][1]), int(matches[0][0]))
            else:
                tasks.append(Task(button_a=a, button_b=b, price=price))
                continue
        tasks.append(Task(button_a=a, button_b=b, price=price))
    return get_the_best_price(a_cost=a_cost, b_cost=b_cost, tasks=tasks)


@timer_decorator
def solve_2(p: Path) -> int:
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
                price = (int(f"10000000000000{matches[0][1]}"), 
                         int(f"10000000000000{matches[0][0]}"))
            else:
                tasks.append(Task(button_a=a, button_b=b, price=price))
                continue
        tasks.append(Task(button_a=a, button_b=b, price=price))
    return get_the_best_price_2(a_cost=a_cost, b_cost=b_cost, tasks=tasks)

if __name__ == '__main__':
    assert solve_1(p=t_f) == 480
    assert solve_1(p=in_f) == 28887
    # print(solve_2(p=t_f))

    print("All passed!")
