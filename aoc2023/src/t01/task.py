import os
import pathlib

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')

# @timer_decorator
def solve_1():
    with open(input_file, 'r', encoding='utf8') as f:
        print(sum(n[0]*10 + n[-1] for n in
                  [[int(c) for c in line.strip() if str(c).isdigit()] for line in f.readlines()]))

def get_number(line: str):
    res = 0
    dic_w = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }

    first_occurments = [(line.find(key), item)
                        for key, item in dic_w.items() if line.find(key) != -1]

    last_occurments = [(len(line) - line[::-1].find(key[::-1]) -1, item)
                        for key, item in dic_w.items() if line[::-1].find(key[::-1]) != -1]


    numbers = [(idx, int(c)) for idx, c in enumerate(line) if str(c).isdigit()]

    res = sorted(first_occurments + last_occurments + numbers, key=lambda x: x[0])
    return res[0][1]*10 + res[-1][1]


def solve_2():
    with open(input_file, 'r', encoding='utf8') as f:
        print(sum((get_number(line=line.strip()) for line in f.readlines())))

if __name__ == '__main__':
    solve_1()
    solve_2()
