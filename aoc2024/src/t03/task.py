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

        matches = [(m.start(0), m.groups()) for m in re.finditer('mul\\((\\d+),(\\d+)\\)', data)]
        n_ids = [(m.start(0)) for m in re.finditer('don\'t\\(\\)', data)]
        y_ids = [0] + [(m.start(0)) for m in re.finditer('do\\(\\)', data)]


        res = 0
        y_id = 0
        n_id = 0
        for m in matches:
            curr_i = m[0]            
            for i in range(y_id, len(y_ids)):
                if y_ids[i] > curr_i:
                    break
                y_id = i
            for j in range(n_id, len(n_ids)):
                if n_ids[j] > curr_i:
                    break
                n_id = j
            if (y_ids[y_id] < curr_i) and (n_ids[n_id] > curr_i) or (n_ids[n_id] < y_ids[y_id]):
                res += int(m[1][0])*int(m[1][1])
        return res


if __name__ == '__main__':
    test_o = solve_1_regex(p=t_f)

    if test_o != 161:
        raise ValueError('Test failed!')
    
    f_o = solve_1_regex(p=in_f)
    if f_o != 173529487:
        raise ValueError('The first task failed!')
    
    test_o = solve_2_regex(p=t_f)
    print(test_o)
    if test_o != 48:
        raise ValueError('Test failed!')
    
    s_o = solve_2_regex(p=in_f)
    if s_o != 99532691:
        raise ValueError('The second task failed!')

    print("All passed!")
