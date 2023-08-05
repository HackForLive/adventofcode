import pathlib
import os

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'input.txt')

def solve_1():
    x = 0
    y = 0
    with open(input_file, 'rt', encoding='utf8') as f:
        for line in f:
            parts = line.strip().split(' ')
            comm = parts[0]
            n = int(parts[1])
            if comm == 'forward':
                x += n
            elif comm == 'up':
                y -= n
            elif comm == 'down':
                y += n
            else:
                raise ValueError('Unexpected command!')
    print(f'{x =}, {y =}')
    print(x * y)

def solve_2():
    x = 0
    y = 0
    aim = 0
    with open(input_file, 'rt', encoding='utf8') as f:
        for line in f:
            parts = line.strip().split(' ')
            comm = parts[0]
            n = int(parts[1])
            if comm == 'forward':
                x += n
                y += aim * n
            elif comm == 'up':
                # y -= n
                aim -= n
            elif comm == 'down':
                # y += n
                aim += n
            else:
                raise ValueError('Unexpected command!')
    print(f'{x =}, {y =}, {aim =}')
    print(x * y)


if __name__ == '__main__':
    solve_1()
    solve_2()
