import pathlib
import os
from typing import List

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

def solve_2():
     with open(input_file, 'rt', encoding='utf8') as f:
        lines = []
        [lines.append(line.strip()) for line in f]

        def get_oxygen_bit(idx: int, bits: List[str]):
            return '1' if len(list(filter(lambda x: x[idx] == '1', bits))) >= len(list(filter(lambda x: x[idx] == '0', bits))) else '0'

        def get_co2_bit(idx: int, bits: List[str]):
            return '0' if len(list(filter(lambda x: x[idx] == '0', bits))) <= len(list(filter(lambda x: x[idx] == '1', bits))) else '1'

        oxygen = lines.copy()
        co2 = lines.copy()
        i: int = 0
        n: int = len(lines[0])
        while i < n:
            oxygen_bit = get_oxygen_bit(idx=i, bits=oxygen)
            co2_bit = get_co2_bit(idx=i, bits=co2)
            
            if len(oxygen) > 1:
                oxygen = list(filter(lambda x: x[i] == oxygen_bit, oxygen))
            if len(co2) > 1:
                co2 = list(filter(lambda x: x[i] == co2_bit, co2))
            i += 1

        oxygen = int(''.join(oxygen),base=2)
        co2 = int(''.join(co2),base=2)
            
        print(f'{oxygen =}, {co2 =}')
        print(oxygen * co2)


if __name__ == '__main__':
    solve_1()
    solve_2()
