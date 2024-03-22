from collections import deque 

from dataclasses import dataclass, field
from enum import Enum
import pathlib
import os
from typing import List, Tuple
import copy

curr_dir = pathlib.Path(__file__).parent.resolve()

@dataclass
class Item:
    x: int
    m: int
    a: int
    s: int


@dataclass
class ItemRange:
    x_min: int
    x_max: int
    m_min: int
    m_max: int
    a_min: int
    a_max: int
    s_min: int
    s_max: int


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

    @property
    def rules(self):
        return self._rules

    def execute(self, item: Item) -> ResultData:
        for rule in self._rules:
            res: ResultData = rule.execute(item=item)
            if res.result == Result.ROUTE and res.data is None:
                continue
            return res


@dataclass
class ItemRangeNode:
    item_range: ItemRange
    work_flow_name: str
    rule_id: int


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


def solve_1(in_f: str) -> int:
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

    return sum(k.x + k.m + k.a + k.s for k in i_r)

def solve_2(in_f: str) -> int:
    _, work_flows = parse(input_file=in_f)

    stack = deque()
    start_item = ItemRange(
        x_min=1, x_max=4000,
        m_min=1, m_max=4000,
        a_min=1, a_max=4000,
        s_min=1, s_max=4000,
    )
    node = ItemRangeNode(
        item_range=start_item,
        work_flow_name='in',
        rule_id=0
    )
    stack.append(node)

    res: List[ItemRange] = []

    while stack:
        curr: ItemRangeNode = stack.pop()

        rule = work_flows[curr.work_flow_name][curr.rule_id]

        if isinstance(rule, RouteWithConditionRule):

            if '>' in rule._condition:
                l, v = rule._condition.split('>')
                mi = getattr(curr.item_range, f'{l}_min')
                ma = getattr(curr.item_range, f'{l}_max')

                "l > v"
                if ma > int(v):
                    ir = copy.deepcopy(curr.item_range)
                    setattr(ir, f'{l}_min', int(v) + 1)
                    if isinstance(rule._rule, AcceptedRule):
                        res.append(ir)
                    elif isinstance(rule._rule, RouteToWorkFlowRule):
                        node = ItemRangeNode(
                            item_range=ir,
                            work_flow_name=rule._rule._work_flow_name,
                            rule_id=0
                        )
                        stack.append(node)
                if mi <= int(v):
                    ir = copy.deepcopy(curr.item_range)
                    setattr(ir, f'{l}_max', int(v))
                    node = ItemRangeNode(
                        item_range=ir,
                        work_flow_name=curr.work_flow_name,
                        rule_id=curr.rule_id+1
                    )
                    stack.append(node)
            elif '<' in rule._condition:
                l, v = rule._condition.split('<')
                mi = getattr(curr.item_range, f'{l}_min')
                ma = getattr(curr.item_range, f'{l}_max')

                "l < v"
                if mi < int(v):
                    ir = copy.deepcopy(curr.item_range)
                    setattr(ir, f'{l}_max', int(v) - 1)
                    if isinstance(rule._rule, AcceptedRule):
                        res.append(ir)
                    elif isinstance(rule._rule, RouteToWorkFlowRule):
                        node = ItemRangeNode(
                            item_range=ir,
                            work_flow_name=rule._rule._work_flow_name,
                            rule_id=0
                        )
                        stack.append(node)
                if ma >= int(v):
                    ir = copy.deepcopy(curr.item_range)
                    setattr(ir, f'{l}_min', int(v))
                    node = ItemRangeNode(
                        item_range=ir,
                        work_flow_name=curr.work_flow_name,
                        rule_id=curr.rule_id+1
                    )
                    stack.append(node)
            else:
                raise ValueError('Unxpected')
        elif isinstance(rule, RouteToWorkFlowRule):
            node = ItemRangeNode(
                item_range=curr.item_range,
                work_flow_name=rule._work_flow_name,
                rule_id=0
            )
            stack.append(node)
        elif isinstance(rule, AcceptedRule):
            res.append(curr.item_range)
    # print(res)
    return sum(
        [(r.x_max-r.x_min+1)*(r.m_max-r.m_min+1)*(r.a_max-r.a_min+1)*(r.s_max-r.s_min+1) 
         for r in res])

if __name__ == '__main__':
    infile = os.path.join(curr_dir, 'test.txt')
    res_1 = solve_1(in_f=infile)
    if res_1 == 362930:
        print(f"Correct answer: {res_1}")
    else:
        print('Wrong answer')

    res_2 = solve_2(in_f=os.path.join(curr_dir, 'test.txt'))

    if res_2 == 116365820987729:
        print(f"Correct answer: {res_2}")
    else:
        print('Wrong answer')
