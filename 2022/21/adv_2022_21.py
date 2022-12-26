import os
from collections import deque

class Node:
    def __init__(self, data: int, left: str, right: str, op: str):
        self.data = data
        self.left = left
        self.right = right
        self.op = op
    
    def doOp(self, nodes):
        if self.op == '*':
            self.data = nodes[self.left].data * nodes[self.right].data
        elif self.op == '/':
            self.data = nodes[self.left].data / nodes[self.right].data
        elif self.op == '+':
            self.data = nodes[self.left].data + nodes[self.right].data
        elif self.op == '-':
            self.data = nodes[self.left].data - nodes[self.right].data
        else:
            raise NotImplemented("No such operation supported")

def resolveRoot(l):
    stack = deque()
    stack.append(l['root'])

    while stack:
        head = stack[-1]
        if head.data:
            stack.pop()
        elif l[head.left].data and l[head.right].data:
            head.doOp(l)
            stack.pop()
        else:
            stack.append(l[head.left])
            stack.append(l[head.right])
    return l['root'].data

if __name__ == "__main__" :

    res: int = 0
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt'), 'r')
    lines = f.readlines()

    l = {}
    n = len(lines)
    for i in range(n):
        parts = lines[i].strip().split(' ')
        if len(parts) == 2:
            l[parts[0][:-1]] = Node(int(parts[1]), None, None, None)
        elif len(parts) == 4:
            l[parts[0][:-1]] = Node(None, parts[1], parts[3], parts[2])
        else:
            raise NotImplemented("No such input supported")

    print(resolveRoot(l))
