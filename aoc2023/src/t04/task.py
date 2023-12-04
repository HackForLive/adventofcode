import os
import pathlib


curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


# @timer_decorator
def solve_1():
    res = 0
    with open(input_file, 'r', encoding='utf8') as f:
        for line in f:
            l = line.strip()
            parts = l.split(':')
            numb = parts[1].strip().split('|')

            winning = set([int(n) for n in numb[0].strip().split(' ') if n.isdigit()])
            curr = [int(n) for n in numb[1].strip().split(' ') if n.isdigit()]

            res += int(pow(2, len(winning.intersection(curr))- 1))
    print(res)


if __name__ == '__main__':
    solve_1()
