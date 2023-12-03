from typing import List, Dict
import re
import os
import pathlib

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'input_test.txt')


with open(input_file, mode='r', encoding='utf-8') as f:
    for line in f:
        regex = re.compile(pattern=r'([:;,])(?:\s*(\d+)\s*(\w+)\s*)*')

        bags: List[Dict[str, int]] = []
        tmp = {}
        for match in regex.finditer(line.strip()):
            if match.group(1) == ';':
                # new set
                bags.append(tmp)
                tmp = {}
            tmp[match.group(3)] = match.group(2)
        if tmp:
            bags.append(tmp)
        print(bags)
