from enum import Enum
import pathlib
import os
from typing import List, Tuple

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'input_test.txt')


class Result(Enum):
    ACCEPTED = 0
    REJECTED = 1
    ROUTED = 2
    PASS = 3

class Item:
    def __init__(self, x: int, m: int, a: int, s: int) -> None:
        self.x = x
        self.m = m
        self.a = a
        self.s = s


class Rule:
    def __init__(self, item: Item, operation: str = None) -> None:
        self.operation = operation
        self.item = item

    def get_result(self) -> Tuple[Result, str]:
        pass

class RoutedRule(Rule):
    def get_result(self) -> Tuple[Result, str]:
        if '<' in self.operation:
            op, w = self.operation.split(':')
            l, r = op.split('<')
            if int(getattr(self.item, l)) < r:
                return Result.ROUTED
            return Result.PASS, w
        elif '>' in self.operation:
            op, w = self.operation.split(':')
            l, r = op.split('>')
            if int(getattr(self.item, l)) > r:
                return Result.ROUTED
            return Result.PASS, w
        else:
            return Result.PASS, self.operation

class AcceptedRule(Rule):
    def get_result(self) -> Tuple[Result, str]:
        return (Result.ACCEPTED, None)

class RejectedRule(Rule):
    def get_result(self) -> Tuple[Result, str]:
        return (Result.REJECTED, None)

class WorkFlow():
    def __init__(self, name: str, rules: List[Rule]):
        self._name = name
        self._rules = rules

    def get_result(self) -> Result:
        for rule in self._rules:
            # we got the result
            if rule.get_result() == Result.ACCEPTED or rule.get_result() == Result.REJECTED:
                return rule.get_result()
            # route to another workflow
            # don't anything not satisfied


def parse():
    with open(input_file, 'r', encoding='utf8') as f:
        rules = {

        }
        parts = []
        
        for line in f:
            c_line = line.strip()
            if c_line == '':
                continue
            
            if c_line.startswith(r'{'):
                parts_dic = {}
                for p in c_line[1:-1].split(','):
                    l, r = p.split('=')
                    parts_dic[l] = r
                parts.append(parts_dic)
            else:
                l, r = c_line.split(r'{')
                rules_raw = r[:-1].split(',')

                rules_res = []
                for rule_raw in rule_raw:
                    if rule_raw == 'A':
                        rules_res.append(AcceptedRule())
                rules[l] = ...


def solve_1():
    matrix = parse()
    offset = 1
    border = -1
    m_offset = get_matrix_with_offset(matrix=matrix, val=border, offset=offset)
    start_pos = (offset,offset)
    start_instr = Instruction(point=start_pos, direction=Direction.EAST, value=m_offset[start_pos])
    start_instr.path_history = []
    print(bfs_with_weights(matrix=m_offset, start_instr=start_instr, shape=matrix.shape))


if __name__ == '__main__':
    solve_1()
    # solve_2()
