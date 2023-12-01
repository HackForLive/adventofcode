import os
import pathlib

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')

# @timer_decorator
def solve_1():
    with open(input_file, 'r', encoding='utf8') as f:
        print(sum(n[0]*10 + n[-1] for n in
                  [[int(c) for c in line.strip() if str(c).isdigit()] for line in f.readlines()]))

if __name__ == '__main__':
    solve_1()
