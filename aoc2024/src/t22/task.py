from __future__ import annotations
from pathlib import Path
from typing import List
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'


def get_generated_secret_number(s: int, time: int) -> int:
    secret = s
    for _ in range(time):
        tmp = (secret * 64)
        secret = tmp ^ secret
        secret = secret % 16777216

        # if secret % 32 < 16:
        #     tmp = (secret//32)
        # else:
        tmp = (secret//32)

        secret = tmp ^ secret
        secret = secret % 16777216

        tmp = (secret*2048)
        secret = tmp ^ secret
        secret = secret % 16777216
    return secret

def get_generated_secret_number_sum(secrets: List[int], time: int) -> int:
    return sum((get_generated_secret_number(s=secret, time=time) for secret in secrets))

def parse(p: Path) -> List[int]:
    with open(p, 'r', encoding='utf8') as f:
        return [int(line.strip()) for line in f]

@timer_decorator
def solve(p: Path, time: int) -> int:
    secrets = parse(p=p)
    return get_generated_secret_number_sum(secrets=secrets, time=time)


if __name__ == '__main__':
    assert solve(p=t_f, time=2000) == 37327623
    assert solve(p=in_f, time=2000) == 13461553007
    print("All passed!")
