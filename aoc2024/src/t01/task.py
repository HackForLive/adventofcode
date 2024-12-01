import functools
from pathlib import Path

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'


@timer_decorator
def solve_1(p: Path):
    with open(p, 'r', encoding='utf8') as f:
        l_l, r_l = zip(*((int(i[0]), int(i[1])) for i in (line.strip().split('   ') for line in f)))

        return functools.reduce(
            lambda a, b: a + b, (abs(i[0] - i[1]) for i in zip(sorted(l_l), sorted(r_l))))


@timer_decorator
def solve_2(p: Path):
    with open(p, 'r', encoding='utf8') as f:
        l_l = []
        r_l = {}
        for line in f:
            l = line.strip()
            le, re = l.split('  ')
            l_l.append(int(le))
            r_l[int(re)] = r_l.get(int(re), 0) + 1

        return functools.reduce(
            lambda a, b: a + b, (l_l[i]*r_l.get(l_l[i], 0) for i in range(len(l_l))))


if __name__ == '__main__':
    test_o = solve_1(p=t_f)
    if test_o != 11:
        raise ValueError('Test failed!')
    
    f_o = solve_1(p=in_f)
    if f_o != 2970687:
        raise ValueError('The first task failed!')
    
    test_o = solve_2(p=t_f)
    if test_o != 31:
        raise ValueError('Test failed!')
    
    s_o = solve_2(p=in_f)
    if s_o != 23963899:
        raise ValueError('The second task failed!')

    print("All passed!")
