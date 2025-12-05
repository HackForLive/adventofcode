from pathlib import Path

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'


def get_fresh(ingred: list[int], ranges: list[tuple[int,int]]) -> int:
    res = 0
    for i in ingred:
        for l, r in ranges:
            if (i >= l) and (i <= r):
                res += 1
                break
    return res

def get_all_fresh_unions(ranges: list[tuple[int,int]]) -> int:
    # union find
    s = sorted(ranges, key=lambda k: k[0])

    res = []

    curr = s[0]
    for i in range(len(s)):
        if s[i] == curr:
            continue
        if curr[1] >= s[i][0]:
            curr = (curr[0], max(curr[1], s[i][1]))
        else:
            res.append(curr)
            curr = s[i]
    if curr:
        res.append(curr)
    
    c = 0
    for i in res:
        c += i[1]-i[0]+1
    return c


@timer_decorator
def solve_1(p: Path):
    ranges = []
    ingred = []
    is_ingred = False
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            line = l.strip()
            if not line:
                is_ingred = True
                continue

            if is_ingred:
                ingred.append(int(line))
            else:
                l,r = line.split('-')
                ranges.append((int(l), int(r)))
    
    return get_fresh(ingred=ingred, ranges=ranges)


@timer_decorator
def solve_2(p: Path):
    ranges = []
    ingred = []
    is_ingred = False
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            line = l.strip()
            if not line:
                is_ingred = True
                continue

            if is_ingred:
                ingred.append(int(line))
            else:
                l,r = line.split('-')
                ranges.append((int(l), int(r)))
    
    return get_all_fresh_unions(ranges=ranges)

if __name__ == '__main__':
    assert solve_1(p=t_f) == 3
    print(solve_1(p=in_f)) # 520
    
    assert solve_2(p=t_f) == 14
    print(solve_2(p=in_f)) # too high 347338785050515
    print("All passed!")
