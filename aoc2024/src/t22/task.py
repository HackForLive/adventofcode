from typing import List, Dict
from pathlib import Path
import itertools

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
 
t_f = curr_dir / 'test.txt'
t2_f = curr_dir / 'test2.txt'
in_f = curr_dir / 'in.txt'

def get_secret(s: int) -> int:
    secret = s
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret//32) ^ secret) % 16777216
    return ((secret*2048) ^ secret) % 16777216


def get_generated_secret_number(s: int, time: int) -> int:
    secret = s
    for _ in range(time):
        secret = get_secret(s=secret)
    return secret


def get_diffs_secret_number(s: int, time: int) -> Dict:
    dic_n = {}
    
    secret = s
    secrets = [secret]
    diffs = []
    
    for _ in range(time):
        tmp = get_secret(s=secret)
        diffs.append((tmp%10)-(secret%10))
        secret = tmp
        secrets.append(secret)
        
    for i in range(3, len(diffs)):
        seq = (diffs[i-3], diffs[i-2], diffs[i-1], diffs[i])
        nu = secrets[i+1]% 10
        if seq not in dic_n:
            dic_n[seq]=nu
    return dic_n

def get_generated_secret_number_sum(secrets: List[int], time: int) -> int:
    return sum((get_generated_secret_number(s=secret, time=time) for secret in secrets))

def parse(p: Path) -> List[int]:
    with open(p, 'r', encoding='utf8') as f:
        return [int(line.strip()) for line in f]

@timer_decorator
def solve(p: Path, time: int) -> int:
    secrets = parse(p=p)
    return get_generated_secret_number_sum(secrets=secrets, time=time)

@timer_decorator
def solve_2(p: Path, time: int) -> int:
    secrets = parse(p=p)
    
    ddp = {}
    for s in secrets:
         dd = get_diffs_secret_number(s=s, time=time)
         for j in set(itertools.chain(dd.keys(), ddp.keys())):
             ddp[j]= dd.get(j, 0) + ddp.get(j, 0)

    return max(ddp.values())


if __name__ == '__main__':
    assert solve(p=t_f, time=2000) == 37327623
    assert solve(p=in_f, time=2000) == 13461553007
    assert solve_2(p=t2_f, time=2000) == 23
    assert solve_2(p=in_f, time=2000) == 1499
    print("All passed!")