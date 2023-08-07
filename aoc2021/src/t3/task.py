import pathlib
import os

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'input.txt')

def solve_1():
    with open(input_file, 'rt', encoding='utf8') as f:
        ones = None
        zeros = None
        for line in f:
            line = line.strip()
            if not ones and not zeros:
                ones = [0 for i in range(len(line))]
                zeros = [0 for i in range(len(line))]
            for idx, c in enumerate(line):
                if c == '0':
                    zeros[idx] += 1
                else:
                    ones[idx] += 1
        
        gamma = ['0' if ones[i] < zeros[i] else '1' for i in range(len(ones))]
        epsilon = ['0' if gamma[i] == '1' else '1' for i in range(len(gamma))]
        
        gamma = int(''.join(gamma),base=2)
        epsilon = int(''.join(epsilon),base=2)
            
        print(f'{gamma =}, {epsilon =}')
        print(gamma * epsilon)

# def solve_2():


if __name__ == '__main__':
    solve_1()
    # solve_2()
