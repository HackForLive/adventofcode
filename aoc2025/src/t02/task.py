from pathlib import Path

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'


def is_symmetric(l: int):
    s = str(l)
    ll = len(s)
    if ll%2 == 0:
        if s[:ll//2] == s[ll//2:]:
            return True 
        return False
    return False


def check(step: int, n: str):
    pat = n[:step]

    if len(n) % len(pat) != 0:
        return False
    
    i = 0
    while i < len(n):
        if n[i:step+i] != pat:
            return False
        i += step

    return True

def is_symmetric_any(l: int):
    s = str(l)
    ll = len(s)

    for i in range(1, ll//2 + 1):
        if check(i, s):
            return True
    return False


@timer_decorator
def solve_1(p: Path):
    c = 0
    with open(p, 'r', encoding='utf8') as f:
        l = f.readlines()[0].strip()
        ranges = [(int(i.split('-')[0]),int(i.split('-')[1])) for  i in l.split(',')]
        for left,right in ranges:
            for l in range(left, right+1):
                if is_symmetric(l):
                    c += l        
    return c

@timer_decorator
def solve_2(p: Path):
    c = 0
    with open(p, 'r', encoding='utf8') as f:
        l = f.readlines()[0].strip()
        ranges = [(int(i.split('-')[0]),int(i.split('-')[1])) for  i in l.split(',')]
        for left,right in ranges:
            for l in range(left, right+1):
                if is_symmetric_any(l):
                    c += l
    return c

if __name__ == '__main__':
    assert solve_1(p=t_f) == 1227775554
    print(solve_1(p=in_f)) # 5398419778
    
    assert solve_2(p=t_f) == 4174379265
    print(solve_2(p=in_f)) # 15704845910
    print("All passed!")
