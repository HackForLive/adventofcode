import pathlib
import os

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'input.txt')

def solve_1():
    curr = None
    res = 0
    with open(input_file, 'rt', encoding='utf8') as f:
        for line in f:
            last = int(line.strip())
            if curr and curr < last:
                res += 1
            curr = last
    print(res)

def solve_2():
    curr = None
    res = 0
    with open(input_file, 'rt', encoding='utf8') as f:
        lines = f.readlines()
        for idx in range(2, len(lines)):


            last = int(lines[idx].strip()) + int(lines[idx-1].strip()) + int(lines[idx-2].strip())
            if curr and curr < last:
                res += 1
            curr = last
    print(res)

if __name__ == '__main__':
    solve_1()
    solve_2()

