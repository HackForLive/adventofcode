from collections import deque 

from abc import abstractmethod, ABCMeta
import pathlib
import os
from enum import Enum, auto
from time import sleep
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
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def receive(self, pulse: Pulse, sender_name: str):
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

    def get_name(self) -> str:
        return self._name

    def receive(self, pulse: Pulse, sender_name: str):
        if pulse == Pulse.HIGH:
            self._pulse = Pulse.NONE
        if pulse == Pulse.LOW:
            self._state[self._name] = not self._state[self._name]
            self._pulse = Pulse.HIGH if self._state[self._name] else Pulse.LOW

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

    def get_name(self) -> str:
        return self._name

    def receive(self, pulse: Pulse, sender_name: str):
        # update state??
        self._state[self._name][sender_name] = pulse == Pulse.HIGH
        self._pulse = Pulse.LOW
        for _ ,v in self._state[self._name].items():
            if not v:
                self._pulse = Pulse.HIGH
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

    def get_name(self) -> str:
        return self._name

    def receive(self, pulse: Pulse, sender_name: str):
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
                states[module]=False
                blue_prints[module]=BroadcastModule
            else:
                m_type = r[0]
                module = r[1:]
                if m_type == '%':
                    states[module] = False
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
                states[v][key] = False


    # print(work_flows)
    # print(states)
    # print(blue_prints)
    return work_flows, states, blue_prints


def solve_1(in_f: str) -> int:
    work_flows, states, blue_prints = parse(input_file=in_f)

    low_signal_c = 0
    high_signal_c = 0

    for _ in range(1000):
        start = blue_prints['broadcaster'](name='broadcaster', state=states)
        q = deque()
        q.append(start)
        start.receive(pulse=Pulse.LOW, sender_name='button')
        low_signal_c += 1
        pulse = None

        while q:
            module = q.popleft()
            pulse = module.send()
            if pulse == Pulse.NONE:
                continue

            receivers = work_flows[module.get_name()]
            # print(module.get_name())
            # print(pulse)
            # print(receivers)
            # print(states)
            if pulse == Pulse.HIGH:
                high_signal_c += len(receivers)
            else:
                low_signal_c += len(receivers)
            for receiver in receivers:
                if receiver not in blue_prints:
                    continue
                r = blue_prints[receiver](name=receiver, state=states)
                r.receive(pulse=pulse, sender_name=module.get_name())
                q.append(r)
            # sleep(.2)
        # print(f"{high_signal_c =}")
        # print(f"{low_signal_c =}")
    return high_signal_c*low_signal_c


def solve_2(in_f: str) -> int:
    work_flows, states, blue_prints = parse(input_file=in_f)
    print(states)

    limit = 1000000000000

    for i in range(limit):
        start = blue_prints['broadcaster'](name='broadcaster', state=states)
        q = deque()
        q.append(start)
        start.receive(pulse=Pulse.LOW, sender_name='button')
        pulse = None

        while q:
            module = q.popleft()
            pulse = module.send()
            if pulse == Pulse.NONE:
                continue

            receivers = work_flows[module.get_name()]
            for receiver in receivers:
                if receiver not in blue_prints:
                    if receiver == 'rx' and pulse == Pulse.LOW:
                        return i
                    continue
                r = blue_prints[receiver](name=receiver, state=states)
                r.receive(pulse=pulse, sender_name=module.get_name())
                q.append(r)
    print(states)
    return -1


if __name__ == '__main__':
    infile = os.path.join(curr_dir, 'input.txt')
    res_1 = solve_1(in_f=infile)
    if res_1 == 681194780:
        print(f"Correct answer: {res_1}")
    else:
        print(f'Wrong answer: {res_1}')

    res_2 = solve_2(in_f=infile)
    if res_2 == 681194780:
        print(f"Correct answer: {res_2}")
    else:
        print(f'Wrong answer: {res_2}')
