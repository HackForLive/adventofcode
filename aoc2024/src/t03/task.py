from pathlib import Path
import functools
import re

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'


def get_pair_multiplication(content: str, idx: int) -> int | None:
    i = idx
    if content[idx] != '(':
        return None

    n1 = []
    n2 = []
    sep = False

    while i < len(content):
        i += 1
        if content[i] == ',':
            if sep:
                return None
            sep = True
        elif content[i].isdigit():
            if sep:
                n2.append(content[i])
            else:
                n1.append(content[i])

        elif content[i] == ')':
            if n1 and n2:
                return int(''.join(n1))*int(''.join(n2))
            else:
                return None
        else:
            return None
        
    return None
        


def parse(content: str):
    i = 0
    res = 0
    while i < len(content) - 4:
        if content[i:i+3] == 'mul':
            i = i+3
            tmp = get_pair_multiplication(content=content, idx=i)
            if tmp is not None:
                res += tmp
        else:
            i += 1
    return res


def parse_2(content: str):
    i = 0
    res = 0
    enable: bool = True
    while i < len(content) - 4:
        if content[i:i+3] == 'mul':
            i = i+3
            if not enable:
                continue 
            tmp = get_pair_multiplication(content=content, idx=i)
            if tmp is not None:
                res += tmp
        elif (i+5 < len(content)) and (content[i:i+4] == "do()"):
            enable = True
            i += 4
        elif (i+8 < len(content)) and (content[i:i+7] == "don't()"):
            enable = False
            i += 7
        else:
            i += 1
    return res


@timer_decorator
def solve_1(p: Path):
    with open(p, encoding='utf-8', mode='r') as file:
        data = file.read().rstrip()
    return parse(content=data)


@timer_decorator
def solve_1_regex(p: Path):
    with open(p, encoding='utf-8', mode='r') as file:
        data = file.read().rstrip()
        
        rgx = re.compile('mul\\((\\d+),(\\d+)\\)')
        return functools.reduce(lambda a, b: a + b, 
                                (int(i[0])*int(i[1]) for i in rgx.findall(data)))


@timer_decorator
def solve_2(p: Path):
    with open(p, encoding='utf-8', mode='r') as file:
        data = file.read().rstrip()
    return parse_2(content=data)


if __name__ == '__main__':
    test_o = solve_1_regex(p=t_f)

    if test_o != 161:
        raise ValueError('Test failed!')
    
    f_o = solve_1_regex(p=in_f)
    if f_o != 173529487:
        raise ValueError('The first task failed!')
    
    test_o = solve_2(p=t_f)
    print(test_o)
    if test_o != 48:
        raise ValueError('Test failed!')
    
    s_o = solve_2(p=in_f)
    if s_o != 99532691:
        raise ValueError('The second task failed!')

    print("All passed!")
