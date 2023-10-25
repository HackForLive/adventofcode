import pathlib
import os
import sys
import functools
import time
from typing import List, Tuple
from functools import partial

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


def cost(numbers: List[int], x: int):
    """
    Cost function for first part
    """
    return sum([abs(x - item) for item in numbers])


def cost_2(numbers: List[int], x: int):
    """
    Cost function for second part
    """
    return sum([((abs(x - item) + 1)*abs(x - item) // 2) for item in numbers])


def custom_binary_search(lookup_arr: List[int], cost_fn) -> Tuple[int, int]:
    """
    We are searching for the minimum
    """
    low = 0
    high = len(lookup_arr) - 1
    mid = 0
    while low <= high:
 
        mid = (high + low) // 2
        
        curr = cost_fn(x=lookup_arr[mid])
        left = cost_fn(x=lookup_arr[mid-1])
        right = cost_fn(x=lookup_arr[mid+1])
        # If x is greater, ignore left half
        # if arr[mid] < x:
        if right < curr and curr < left:
            low = mid + 1
 
        # If x is smaller, ignore right half
        # elif arr[mid] > x:
        elif right > curr and curr > left:
            high = mid - 1
 
        # means x is present at mid
        else:
            # return mid
            return curr, mid
 
    # If we reach here, then the element was not present
    return -1
 

def timer_decorator(func):
    functools.wraps(func)
    def with_timer(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        elapsed = t1 - t0

        print(f"@timer: {func.__name__} took {elapsed:0.4f} seconds")
        
        return result
    return with_timer


# O(n^2) time, O(n) memory
@timer_decorator
def solve_1():
    res: int = sys.maxsize
    res_number = sys.maxsize
    with open(input_file, 'rt', encoding='utf8') as f:
        numbers = [int(n) for n in f.read().strip().split(',')]
        for number in range(min(numbers), max(numbers)):
            tmp = cost(numbers=numbers, x=number)
            if tmp < res:
                res = tmp
                res_number = number
    print(f"result: {res}")
    print(f"number: {res_number}")


# O(nlong(n)) time, O(n) memory
@timer_decorator
def solve_1_improved():
    with open(input_file, 'rt', encoding='utf8') as f:
        numbers = [int(n) for n in f.read().strip().split(',')]
        print(custom_binary_search(lookup_arr=list(range(min(numbers), max(numbers))),
                                   cost_fn=partial(cost, numbers=numbers)))


@timer_decorator
def solve_2():
    res: int = sys.maxsize
    res_number = sys.maxsize
    with open(input_file, 'rt', encoding='utf8') as f:
        numbers = [int(n) for n in f.read().strip().split(',')]
        
        for number in range(min(numbers), max(numbers)):
            tmp = cost_2(numbers=numbers, x=number)
            if tmp < res:
                res = tmp
                res_number = number
    print(f"result: {res}")
    print(f"number: {res_number}")


# O(nlong(n)) time, O(n) memory
@timer_decorator
def solve_2_improved():
    with open(input_file, 'rt', encoding='utf8') as f:
        numbers = [int(n) for n in f.read().strip().split(',')]
        print(custom_binary_search(lookup_arr=list(range(min(numbers), max(numbers))),
                                   cost_fn=partial(cost_2, numbers=numbers)))


if __name__ == '__main__':
    solve_1()
    solve_1_improved()
    solve_2()
    solve_2_improved()
