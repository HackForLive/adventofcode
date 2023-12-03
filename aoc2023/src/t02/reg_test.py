from typing import List, Dict
import re
import os
import pathlib

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'input_test.txt')


def check(name: str, val: int):
    dic_vals = {
        'red': 12,
        'green': 13,
        'blue': 14
    }

    if dic_vals[name] < val:
        return False
    return True


def solve_1() -> List[Dict[str, int]]:
    with open(input_file, mode='r', encoding='utf-8') as f:
        res_sum = 0
        for line in f:
            regex = re.compile(pattern=r'([:;,])(?:\s*(\d+)\s*(\w+)\s*)*')
            regex_game_id = re.compile(pattern=r'(\d+)')
            game_id = int(regex_game_id.search(line.strip())[0])
            res = True

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

            for bag in bags:
                for item in bag.keys():
                    if not check(name=item, val=int(bag[item])):
                        res = False
                        break
                if not res:
                    break
            if res:
                res_sum +=  game_id
    print(res_sum)

solve_1()
