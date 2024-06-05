from collections import deque 

from abc import abstractmethod, ABCMeta
import pathlib
import os
from enum import Enum, auto
from typing import List

curr_dir = pathlib.Path(__file__).parent.resolve()


class Pulse(Enum):
    """
    Pulse could be either low or high
    """
    LOW  = auto()
    HIGH = auto()
    NONE = auto()

class ModuleInterface(metaclass=ABCMeta):
    """
    Module interface
    """
    @abstractmethod
    def __init__(self, name, state) -> None:
        raise NotImplementedError

    @abstractmethod
    def receive(self, pulse: Pulse):
        raise NotImplementedError

    @abstractmethod
    def send(self):
        raise NotImplementedError


class FlipFlopModule(ModuleInterface):
    """
    has two states on/off
    intially off state

    if receives high pulse, ignores it and nothing happens
    if receives low pulse, flips between on/off
    off -> on -> high pulse
    on -> off -> low pulse
    """
    def __init__(self, name, state) -> None:
        self._name = name
        self._state = state
        self._pulse = Pulse.NONE

    def receive(self, pulse: Pulse):
        if pulse == Pulse.HIGH:
            self._pulse = Pulse.NONE
        if pulse == Pulse.LOW:
            self._state[self._name] = not self._state
            self._pulse = Pulse.HIGH if self._state else Pulse.LOW

    def send(self):
        return self._pulse


class ConjuctionModule(ModuleInterface):
    """
    track last pulse from inputs
    intially all low, it tracks them in memory
    
    if all high pulses, sends low pulse otherwise high pulse
    """
    def __init__(self, name, state) -> None:
        self._name = name
        self._state = state
        self._pulse = Pulse.NONE

    def receive(self, pulse: Pulse):
        # update state??
        self._pulse = Pulse.HIGH
        for _ ,v in self._state[self._name].items():
            if v == 0:
                self._pulse = Pulse.LOW
                break

    def send(self):
        return self._pulse


class BroadcastModule(ModuleInterface):
    """
    same pulse broadcasts to registered modules
    """
    def __init__(self, name, state) -> None:
        self._name = name
        self._state = state
        self._pulse = Pulse.NONE

    def receive(self, pulse: Pulse):
        self._pulse = pulse

    def send(self):
        return self._pulse


def parse(input_file: str):
    with open(input_file, 'r', encoding='utf8') as f:

        # register targets
        # start workflow until reaching loop -> count until ...

        work_flows = {}
        conjunctions = set()
        states = {}
        blue_prints = {}

        for line in f:
            c_line = line.strip()
            if c_line == '':
                continue

            r, l = [o.strip() for o in c_line.split('->')]

            receivers = [o.strip() for o in l.split(',')]

            if r == 'broadcaster':
                module=r
                states[module]=0
                blue_prints[module]=BroadcastModule
            else:
                m_type = r[0]
                module = r[1:]
                if m_type == '%':
                    states[module] = 0
                    blue_prints[module]=FlipFlopModule
                if m_type == '&':
                    # remember conjunctions
                    conjunctions.add(module)
                    blue_prints[module]=ConjuctionModule
                    states[module] = {}

            work_flows[module] = receivers

    # populate conjunctions
    for key, val in work_flows.items():
        for v in val:
            if v in conjunctions:
                states[v][key] = 0


    print(work_flows)
    print(states)
    print(blue_prints)
    return work_flows, states, blue_prints


def solve_1(in_f: str) -> int:
    work_flows, states, blue_prints = parse(input_file=in_f)
    return 0


def solve_2(in_f: str) -> int:
    _, work_flows = parse(input_file=in_f)


if __name__ == '__main__':
    infile = os.path.join(curr_dir, 'test.txt')
    res_1 = solve_1(in_f=infile)
    if res_1 == 362930:
        print(f"Correct answer: {res_1}")
    else:
        print('Wrong answer')
