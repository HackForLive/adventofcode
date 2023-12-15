from __future__ import annotations
from enum import Enum
import os
import pathlib
from typing import List
from collections import OrderedDict


curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')

class Action(Enum):
    REMOVE = 1
    ADD = 2

class Item:
    def __init__(self, name, item_hash: int, focal_len: int, action: Action) -> None:
        self.name = name
        self.item_hash = item_hash
        self.focal_len = focal_len
        self.action = action

def parse() -> List[str]:
    with open(input_file, 'r', encoding='utf8') as f:
        return f.readlines()[0].strip().split(',')

def get_hash_code(record: str) -> int:
    r_hash = 0
    for c in record:
        r_hash = ((r_hash + ord(c))*17)%256
    return r_hash

def solve_1():
    records = parse()
    res = sum((get_hash_code(record=record) for record in records))
    print(res)

def get_items(records: List[str]):
    items = []
    for r in records:
        if '-' in r:
            name = get_hash_code(record=r[:-1])
            items.append(Item(name=r[:-1], item_hash=name, focal_len=-1, action=Action.REMOVE))
        elif '=' in r:
            name = get_hash_code(record=r.split('=')[0])
            items.append(Item(name=r.split('=')[0], item_hash=name, focal_len=int(r.split('=')[1]),
                              action=Action.ADD))
        else:
            raise ValueError('error')
    return items

def solve_2():
    item_dic = {}
    records = parse()
    items = get_items(records=records)

    for item in items:
        if item.action == Action.ADD:
            if item.item_hash in item_dic:
                item_dic[item.item_hash][item.name] = item.focal_len
            else:
                item_dic[item.item_hash] = OrderedDict([(item.name, item.focal_len)])
        elif item.action == Action.REMOVE:
            if item.item_hash in item_dic:
                if item.name in item_dic[item.item_hash]:
                    item_dic[item.item_hash].pop(item.name)
        else:
            raise ValueError('error')

    # print(item_dic)
    res = 0
    for key, val in item_dic.items():
        i = 1
        for k, v in val.items():
            res += (key + 1)*i*v
            i += 1
    print(res)


if __name__ == '__main__':
    solve_1()
    solve_2()
