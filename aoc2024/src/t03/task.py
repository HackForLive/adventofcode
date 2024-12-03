from pathlib import Path
import functools
import re

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'


@timer_decorator
def solve_1_regex(p: Path):
    with open(p, encoding='utf-8', mode='r') as file:
        data = file.read().rstrip()
        
        rgx = re.compile('mul\\((\\d+),(\\d+)\\)')
        return functools.reduce(lambda a, b: a + b, 
                                (int(i[0])*int(i[1]) for i in rgx.findall(data)))

@timer_decorator
def solve_2_regex(p: Path):
    with open(p, encoding='utf-8', mode='r') as file:
        data = file.read().rstrip()

        res = 0
        enabled = True
        for m in re.findall('(do\\(\\))|(don\'t\\(\\))|mul\\((\\d+),(\\d+)\\)', data):
            if m[0] == 'do()':
                enabled = True
            elif m[1] == 'don\'t()':
                enabled = False
            else:
                res = res + int(m[2])*int(m[3]) if enabled else res
        return res


if __name__ == '__main__':
    test_o = solve_1_regex(p=t_f)

    if test_o != 161:
        raise ValueError('Test failed!')
    
    f_o = solve_1_regex(p=in_f)
    if f_o != 173529487:
        raise ValueError('The first task failed!')
    
    test_o = solve_2_regex(p=t_f)
    if test_o != 48:
        raise ValueError('Test failed!')
    
    s_o = solve_2_regex(p=in_f)
    if s_o != 99532691:
        raise ValueError('The second task failed!')

    print("All passed!")
