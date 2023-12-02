import os
import pathlib

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')

# @timer_decorator
def solve_1():
    with open(input_file, 'r', encoding='utf8') as f:
        print(sum(n[0]*10 + n[-1] for n in
                  [[int(c) for c in line.strip() if str(c).isdigit()] for line in f.readlines()]))

def find_first_and_last(line: str):
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

    first_i = len(line)
    first_n = len(line)
    last_i = -1
    last_n = -1
    reverted_line = line[::-1]

    for key, item in dic_w.items():
        f = line.find(key)
        if f >= 0 and f < first_i:
            first_i = f
            first_n = item

        l = reverted_line.find(key[::-1])
        if l >= 0 and len(line) - l - 1 > last_i:
            last_i = len(line) - l - 1
            last_n = item


    numbers = [(idx, int(c)) for idx, c in enumerate(line) if str(c).isdigit()]
    if numbers and numbers[0][0] < first_i:
        res += 10*numbers[0][1]
    else:
        res += 10*first_n

    if numbers and numbers[-1][0] > last_i:
        res += numbers[-1][1]
    else:
        res += last_n
    return res


def solve_2():
    with open(input_file, 'r', encoding='utf8') as f:
        print(sum((find_first_and_last(line=line.strip()) for line in f.readlines())))

if __name__ == '__main__':
    solve_2()
