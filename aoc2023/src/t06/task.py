import os
import pathlib

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


def parse_2():

    with open(input_file, 'r', encoding='utf8') as f:
        lines = f.readlines()

        idl = 0
        times = []
        distance = []
        while idl < len(lines):
            if 'Time:' in lines[idl]:
                times = [n.strip() for n in lines[idl].split(' ')[1:] if n.strip().isdigit()]
            elif 'Distance:' in lines[idl]:
                distance = [n.strip() for n in lines[idl].split(' ')[1:]
                            if n.strip().isdigit()]
            idl = idl + 1

    return int(''.join(times)), int(''.join(distance)) 


def parse_1():

    with open(input_file, 'r', encoding='utf8') as f:
        lines = f.readlines()

        idl = 0
        times = []
        distance = []
        while idl < len(lines):
            if 'Time:' in lines[idl]:
                times = [int(n.strip()) for n in lines[idl].split(' ')[1:] if n.strip().isdigit()]
            elif 'Distance:' in lines[idl]:
                distance = [int(n.strip()) for n in lines[idl].split(' ')[1:] 
                            if n.strip().isdigit()]
            idl = idl + 1

    return list(zip(times, distance))

def solve_1():
    time_dist = parse_1()
    # print(time_dist)
    res_sum = 1
    for t_d in time_dist:
        time = t_d[0]
        dist = t_d[1]
        # try every time, exlude 0 and last
        n = 0
        for t in range(1, time, 1):
            if (time - t)*t > dist:
                n = n + 1
        # print(n)
        res_sum *= n
    print(res_sum)

# TODO : solve with binary search -> O(n) to O(log(n))
def solve_2():
    time, dist = parse_2()
    # print(time, dist)

        # try every time, exlude 0 and last
    n = 0
    for t in range(1, time, 1):
        if (time - t)*t > dist:
            n = n + 1
    print(n)
    # 71503
    # too low

if __name__ == '__main__':
    solve_1()
    solve_2()
