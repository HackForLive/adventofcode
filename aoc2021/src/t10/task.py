import time
import os
import functools
import pathlib
from enum import Enum
from dataclasses import dataclass

from collections import deque
from line_profiler import LineProfiler


curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')

class BracketType(Enum):
    """
    Bracket type, e.g. ( - open and ) - close
    """
    CLOSE = 0
    OPEN = 1


class BracketName(Enum):
    """
    Bracket name, e.g. () - round
    """
    ROUND = 0
    SQUARED = 1
    CURLY = 2
    ANGLED = 3


@dataclass
class Bracket:
    """
    Bracket data class
    """
    name: BracketName
    type: BracketType
    score: int


def get_scoring_1():
    return {
        BracketName.ROUND: 3,
        BracketName.SQUARED: 57,
        BracketName.CURLY: 1197,
        BracketName.ANGLED: 25137
    }


def get_scoring_2():
    return {
        BracketName.ROUND: 1,
        BracketName.SQUARED: 2,
        BracketName.CURLY: 3,
        BracketName.ANGLED: 4
    }


def create_bracket(bracket: str, score_dic) -> Bracket:
    bracket_obj = None
    if bracket == '(':
        bracket_obj = Bracket(name=BracketName.ROUND, type=BracketType.OPEN,
                              score=score_dic[BracketName.ROUND])
    elif bracket == ')':
        bracket_obj = Bracket(name=BracketName.ROUND, type=BracketType.CLOSE,
                              score=score_dic[BracketName.ROUND])
    elif bracket == '[':
        bracket_obj = Bracket(name=BracketName.SQUARED, type=BracketType.OPEN,
                              score=score_dic[BracketName.SQUARED])
    elif bracket == ']':
        bracket_obj = Bracket(name=BracketName.SQUARED, type=BracketType.CLOSE,
                              score=score_dic[BracketName.SQUARED])
    elif bracket == '{':
        bracket_obj = Bracket(name=BracketName.CURLY, type=BracketType.OPEN,
                              score=score_dic[BracketName.CURLY])
    elif bracket == '}':
        bracket_obj = Bracket(name=BracketName.CURLY, type=BracketType.CLOSE,
                              score=score_dic[BracketName.CURLY])
    elif bracket == '<':
        bracket_obj = Bracket(name=BracketName.ANGLED, type=BracketType.OPEN,
                              score=score_dic[BracketName.ANGLED])
    elif bracket == '>':
        bracket_obj = Bracket(name=BracketName.ANGLED, type=BracketType.CLOSE,
                              score=score_dic[BracketName.ANGLED])
    else:
        raise NotImplementedError(f"Bracket name: {bracket} is not implemented yet!")

    return bracket_obj


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


def corrupted_bracket_pricer(line: str) -> int:
    if not line:
        return 0
    stack = deque()
    for c in line:
        bracket = create_bracket(c, score_dic=get_scoring_1())
        if bracket.type == BracketType.CLOSE:
            if len(stack) == 0:
                return 0
            last_bracket: Bracket = stack.pop()
            if last_bracket.name is not bracket.name:
                return bracket.score
        else:
            stack.append(bracket)

    return 0

def incomplete_bracket_pricer(line: str) -> int:
    if not line:
        return 0
    stack = deque()
    for c in line:
        bracket = create_bracket(c, score_dic=get_scoring_2())
        if bracket.type == BracketType.CLOSE:
            if not stack:
                return 0
            last_bracket: Bracket = stack.pop()
            if last_bracket.name is not bracket.name:
                return 0
        else:
            stack.append(bracket)

    # incomplete only
    res = 0
    # print([x.name.name for x in list(stack)])
    while stack:
        res = res * 5 + stack.pop().score

    return res

def solve_1():
    with open(input_file, 'r', encoding='utf8') as f:
        res = sum((corrupted_bracket_pricer(line.strip()) for line in f.readlines()))
        print(res)


def solve_2():
    with open(input_file, 'r', encoding='utf8') as f:
        res = sorted(filter(lambda x: x > 0,
                            (incomplete_bracket_pricer(line.strip()) for line in f.readlines())))
        print(res[len(res)//2])


if __name__ == '__main__':
    solve_1()
    solve_2()
    lp = LineProfiler()
    lp.add_function(incomplete_bracket_pricer)
    # lp.add_function(create_bracket)
    lp_wrapper = lp(solve_2)
    lp_wrapper()
    lp.print_stats()
