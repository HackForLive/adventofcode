from typing import List, Dict
from pathlib import Path
from collections import deque
from dataclasses import dataclass
from abc import ABC, abstractmethod

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
 
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'
ine_f = curr_dir / 'in_e.txt'

states: Dict[str, bool | None]= {}

@dataclass
class Gate(ABC):
    left: str
    right: str
    output: str
    
    @abstractmethod
    def exec(self) -> bool:
        pass
    def can_exec(self):
        return states[self.left] is not None and states[self.right] is not None
    
@dataclass(init=True)
class XorGate(Gate):   
    def exec(self):
        return states[self.left] ^ states[self.right]
            
@dataclass(init=True)
class AndGate(Gate):   
    def exec(self):
        return states[self.left] & states[self.right]
        
@dataclass(init=True)
class OrGate(Gate):   
    def exec(self):
        return states[self.left] | states[self.right]

def parse(p: Path) -> List[Gate]:
    global states
    states = {}

    gates = list()
    is_g = False
    with open(p, 'r', encoding='utf8') as f:
        for line in f:
            l = line.strip()
            if not l:
                is_g = True
                continue
            if not is_g:
                inp, val = l.split(':')
                states[inp.strip()] =bool(int(val.strip()))
            else:
                g, outp = l.split('->')
                if 'XOR' in g:
                    left, right = g.split('XOR')
                    gate = XorGate(left=left.strip(), right=right.strip(), output=outp.strip())
                elif 'OR' in g:
                    left, right = g.split('OR')
                    gate = OrGate(left=left.strip(), right=right.strip(), output=outp.strip())
                elif 'AND' in g:
                    left, right = g.split('AND')
                    gate = AndGate(left=left.strip(), right=right.strip(), output=outp.strip())
                
                left = left.strip()
                right = right.strip()
                outp = outp.strip()
                if left not in states:
                    states[left] = None
                if right not in states:
                    states[right] = None
                if outp not in states:
                    states[outp] = None
                gates.append(gate)
        return gates

def solve(p: Path) -> int:
    gates = parse(p=p)
    
    q = deque(gates)
    while q:
        c = q.popleft()
        
        if c.can_exec():
            states[c.output] = c.exec()
        else:
            q.append(c)
    
    #print(gates)
    bits = [str(int(states[k])) for k in sorted(states.keys(), reverse=True) if k.startswith('z')]
    return int(''.join(bits), 2)

@timer_decorator
def solve_2_check(p: Path) -> int:

    swaps = [ 
        ('bpt', 'krj'),
        ('z31', 'mfm'),
        ('z11', 'ngr'),
        ('z06', 'fkp'),
    ]

    gates = parse(p=p)

    for s in swaps:
        swapped = False
        for g in gates:
            for l in gates:
                if g.output == s[0] and l.output == s[1]:
                    g.output = s[1]
                    l.output = s[0]
                    swapped = True
                    break
            if swapped:
                break
                    
    q = deque(gates)
    while q:
        c = q.popleft()
        
        if c.can_exec():
            states[c.output] = c.exec()
        else:
            q.append(c)
    
    #print(gates)

    x_bits = [str(int(states[k])) for k in sorted(states.keys(), reverse=True) if k.startswith('x')]
    y_bits = [str(int(states[k])) for k in sorted(states.keys(), reverse=True) if k.startswith('y')]
    z_bits = [str(int(states[k])) for k in sorted(states.keys(), reverse=True) if k.startswith('z')]

    x = int(''.join(x_bits))
    y = int(''.join(y_bits))
    z = int(''.join(z_bits))

    x2 = int(''.join(x_bits), 2)
    y2 = int(''.join(y_bits), 2)
    z2 = int(''.join(z_bits), 2)
    print(f"{x2 =} , {y2 =}")

    zz = bin(x2 + y2)

    print(f"{x=} , {y=}, {z=}")
    print(f"{zz}")
    print(f"{bin(z2)}")
    zor = int(zz,2) ^ z2
    
    res = bin(zor)[2:].zfill(len(zz)-2)
    print(res)
    for ii, i in enumerate(res):
        if i == '1':
            print(f"{len(res) -1 - ii =}")
    return int(res)
   
@timer_decorator
def solve_2(p: Path) -> str:
    gates = parse(p=p)

    dd = {}
    for g in gates:
        out = g.output
        l = g.left
        r = g.right

        if isinstance(g, XorGate):
            dd[out]=f"({l} XOR {r})"
        if isinstance(g, AndGate):
            dd[out]=f"({l} AND {r})"
        if isinstance(g, OrGate):
            dd[out]=f"({l} OR {r})"
    
    for k, v in dd.items():
        for k2, v2 in dd.items():   
            if k in v2:
                dd[k2] = v2.replace(k, v)


    # print(dict(sorted(dd.items())))
    for k, v in dict(sorted(dd.items())).items():
        if k.startswith('z0'):
            print(f"{k =} {v=}")
        # if k in ['z38']:
            # print(f"{k =} {v=}")

    # first pair
    #     
    # 'z06' => should be placed on output with xor
    # candidate => 'fkp'

    # wvr XOR jgw -> fkp
    # shc OR bkk -> wvr
    # x06 XOR y06 -> jgw
    # x05 AND y05 -> bkk
    # ffn AND rdj -> shc
    # x05 XOR y05 -> ffn
    # cjp OR ptd -> rdj

    # z06 <=> fkp


    # second pair
    # 'z11' next or is replace with XOR
    # 'candidate' => 'ngr'

    # stv AND jpp -> z11
    # jpp XOR stv -> ngr
    # sgv OR qnf -> stv
    # x11 XOR y11 -> jpp
    # y10 AND x10 -> qnf
    # rvw AND dtb -> sgv
    # z11 <=> ngr

    # 'z31'
    # y31 AND x31
    # mfm
    # mgq XOR tpf -> mfm
    # gqt OR bbk -> tpf
    # x31 XOR y31 -> mgq
    # z31 <=> mfm

    # ntr XOR bpt -> z38
    # y38 AND x38 -> bpt
    # kvd OR snc -> ntr
    # y38 XOR x38 -> krj
    # krj <=> bpt
    swaps = [ 
        ('bpt', 'krj'),
        ('z31', 'mfm'),
        ('z11', 'ngr'),
        ('z06', 'fkp'),
    ]
    a, b = zip(*swaps)
    
    return ','.join(sorted(a+b))

if __name__ == '__main__':
    assert solve(p=t_f) == 2024
    assert solve(p=in_f) == 59619940979346
    assert solve_2(p=in_f) == 'bpt,fkp,krj,mfm,ngr,z06,z11,z31'
    assert solve_2_check(p=in_f) == 0
    print("All passed!")
