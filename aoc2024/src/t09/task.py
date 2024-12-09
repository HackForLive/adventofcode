from collections import deque
from attr import dataclass

from pathlib import Path
from typing import List
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

@dataclass(init=True, frozen=True)
class Block:
    length: int
    allocated: bool
    identifier: int


def get_file_system_check_after_move(line: str) -> int:
    
    dll = deque()
    dll_final = deque()
    
    ii = 0
    for i, c in enumerate(line):
        if i % 2 == 0:
            dll.append(Block(length=int(c), allocated=True, identifier=ii))
            ii += 1
        else:
            dll.append(Block(length=int(c), allocated=False, identifier=0))

    # while dll:
    #     curr: Block = dll.popleft()
    #     print(curr)

    # return 0
    while dll:
        # left one
        curr: Block = dll.popleft()
        
        if curr.allocated:
            dll_final.append(curr)
        else:
            # empty
            size = curr.length
            while size > 0 and dll:
                curr_r : Block = dll.pop()
                if not curr_r.allocated:
                    continue
                else:
                    if (size - curr_r.length) >= 0:
                        dll_final.append(curr_r)
                        size -= curr_r.length
                    else:
                        dll_final.append(Block(length=size, allocated=True, identifier=curr_r.identifier))
                        dll.append(Block(length=curr_r.length - size, allocated=True, identifier=curr_r.identifier))
                        break

    res = 0
    k = 0
    while dll_final:
        curr: Block = dll_final.popleft()
        
        for i in range(curr.length):            
            res += curr.identifier * k
            k += 1

    return res
                    


@timer_decorator
def solve_1(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        for line in f:
            return get_file_system_check_after_move(line=line.strip())
    
@timer_decorator
def solve_2(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        for line in f:
            return get_file_system_check_after_move(line=line.strip())
 

if __name__ == '__main__':
    assert solve_1(p=t_f) == 1928
    assert solve_1(p=in_f) == 6356833654075
    # assert solve_2(p=t_f) == 11387
    # assert solve_2(p=in_f) == 59002246504791
    print("All passed!")
