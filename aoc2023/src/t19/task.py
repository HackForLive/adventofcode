from dataclasses import dataclass, field
from enum import Enum
import pathlib
import os
from typing import List, Tuple

curr_dir = pathlib.Path(__file__).parent.resolve()

@dataclass
class Item:
    x: int
    m: int
    a: int
    s: int


class Result(Enum):
    ACCEPTED = 0
    REJECTED = 1
    ROUTE = 2

class ResultData():
    def __init__(self, result: Result, data: str) -> None:
        self._result = result
        self._data = data

    @property
    def result(self) -> Result:
        return self._result

    @property
    def data(self) -> str:
        return self._data

class GreaterCompator:
    def __init__(self, ) -> None:
        pass


class Rule:
    def execute(self, item: Item) -> ResultData:
        pass

class AcceptedRule(Rule):
    def execute(self, item: Item) -> ResultData:
        return ResultData(result=Result.ACCEPTED, data=None)
    
class RejectedRule(Rule):
    def execute(self, item: Item) -> ResultData:
        return ResultData(result=Result.REJECTED, data=None)
    
class RouteToWorkFlowRule(Rule):
    def __init__(self, work_flow_name) -> None:
        self._work_flow_name = work_flow_name

    def execute(self, item: Item) -> ResultData:
        return ResultData(result=Result.ROUTE, data=self._work_flow_name)


class RouteWithConditionRule(Rule):
    def __init__(self, condition: str, rule: Rule) -> None:
        self._condition = condition
        self._rule = rule

    def execute(self, item: Item) -> ResultData:
        # here we need to pass XMAS
        c:str = self._condition.replace('x', str(item.x)).replace('m', str(item.m)).replace(
            'a', str(item.a)
            ).replace(
            's', str(item.s)
            )
        res: bool = bool(eval(c))
        if res:
            return self._rule.execute(item=item)
        return ResultData(result=Result.ROUTE, data=None)


def parse_rule(raw_rule: str) -> Rule:
    if raw_rule == 'A':
        return AcceptedRule()
    if raw_rule == 'R':
        return RejectedRule()
    if ':' in raw_rule:
        condition, raw_result = raw_rule.split(':')
        rule = parse_rule(raw_rule=raw_result)
        return RouteWithConditionRule(condition=condition, rule=rule)

    return RouteToWorkFlowRule(work_flow_name=raw_rule)


class WorkFlow():
    def __init__(self, name: str, rules: List[Rule]):
        self._name = name
        self._rules = rules

    def execute(self, item: Item) -> ResultData:
        for rule in self._rules:
            res: ResultData = rule.execute(item=item)
            if res.result == Result.ROUTE and res.data is None:
                continue
            return res


def parse(input_file: str):
    with open(input_file, 'r', encoding='utf8') as f:
        work_flows = {}
        items = []

        for line in f:
            c_line = line.strip()
            if c_line == '':
                continue

            if c_line.startswith(r'{'):
                x, m, a, s = c_line[1:-1].split(",")
                x = int(x.split("=")[1])
                m = int(m.split("=")[1])
                a = int(a.split("=")[1])
                s = int(s.split("=")[1])
                items.append(Item(x=x, m=m, a=a, s=s))
            else:
                l, r = c_line.split("{")
                work_flows_raw = r[:-1].split(',')

                rules = [parse_rule(raw_rule=r) for r in work_flows_raw]
                work_flows[l] = rules
        return items, work_flows


def solve_1(in_f: str):
    items, work_flows = parse(input_file=in_f)

    i_r = []
    for _, item in enumerate(items):
        w = WorkFlow(name='in', rules=work_flows['in'])
        res_data = w.execute(item=item)

        while res_data.result == Result.ROUTE:
            w = WorkFlow(name=res_data.data, rules=work_flows[res_data.data])
            res_data = w.execute(item=item)

        if res_data.result == Result.ACCEPTED:
            i_r.append(item)

    print(sum(k.x + k.m + k.a + k.s for k in i_r))

if __name__ == '__main__':
    # infile = os.path.join(curr_dir, 'input_test.txt')
    # solve_1(in_f=infile)
    infile = os.path.join(curr_dir, 'test.txt')
    solve_1(in_f=infile)
