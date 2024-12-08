from collections import deque
import functools
from pathlib import Path
from typing import List
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

def traverse(result: int, nums: List[int], ops: List[str]) -> int:
    q = deque([nums[0]])

    for i in range(1, len(nums)):
        q_tmp = deque()
        while q:
            curr = q.pop()
            if curr > result:
                continue
            for o in ops:
                if o == '*': 
                    tmp = curr*nums[i]
                elif o == '+':
                    tmp = curr+nums[i]
                elif o == '||':
                    tmp = int(f"{curr}{nums[i]}")
                if tmp == result and i == len(nums) - 1:
                    return result
                q_tmp.append(tmp)
        q = q_tmp
    return 0


@timer_decorator
def solve_1(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        res = []
        nums = []
        for line in f:
            res_str, nums_str = line.strip().split(':')
            res.append(int(res_str))
            nums.append([int(i) for i in nums_str.split(' ') if i])
            ops = ['*', '+']
        return functools.reduce(
            lambda a, b: a + b, [traverse(result=r, nums=n, ops=ops) for r, n in zip(res, nums)], 0)
    
@timer_decorator
def solve_2(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        res = []
        nums = []
        for line in f:
            res_str, nums_str = line.strip().split(':')
            res.append(int(res_str))
            nums.append([int(i) for i in nums_str.split(' ') if i])
            ops = ['*', '+', '||']
        return functools.reduce(
            lambda a, b: a + b, [traverse(result=r, nums=n, ops=ops) for r, n in zip(res, nums)], 0)
 

if __name__ == '__main__':
    assert solve_1(p=t_f) == 3749
    assert solve_1(p=in_f) == 6083020304036
    assert solve_2(p=t_f) == 11387
    assert solve_2(p=in_f) == 59002246504791
    print("All passed!")
