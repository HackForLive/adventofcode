from pathlib import Path

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'


@timer_decorator
def solve_1(p: Path):
    pos = 50
    counter = 0
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            line = l.strip()
            d = line[0]
            l = int(line[1:])
            mult = 1 if d == 'R' else -1
            pos = (pos + mult*l)%100
            counter = counter + 1 if pos == 0 else counter
    return counter


@timer_decorator
def solve_2(p: Path):
    pos = 50
    counter = 0
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            line = l.strip()
            d = line[0]
            l = int(line[1:])
            mult = 1 if d == 'R' else -1

            cross = 0
            if mult == 1:
                if pos + mult*l >= 100:
                    cross = (pos + mult*l)//100
                
            else:
                if pos + mult*l <= 0:
                    pp = 1 if pos != 0 else 0
                    cross =  -int(((pos + mult*l)/100)) + pp
            pos = (pos + mult*l)%100

            counter = counter + cross
    return counter

if __name__ == '__main__':
    assert solve_1(p=t_f) == 3
    assert solve_1(p=in_f) == 1158
    
    assert solve_2(p=t_f) == 6
    assert solve_2(p=in_f) == 6860
    print("All passed!")
