import os
from collections import deque

class Node:
    def __init__(self, name: str, data: int, left: str, right: str, op: str):
        self.name = name
        self.data = data
        self.left = left
        self.right = right
        self.op = op
        self.visited = False
    
    def doOp(self, nodes):
        if self.op == '*':
            self.data = int(nodes[self.left].data * nodes[self.right].data)
        elif self.op == '/':
            self.data = int(nodes[self.left].data / nodes[self.right].data)
        elif self.op == '+':
            self.data = int(nodes[self.left].data + nodes[self.right].data)
        elif self.op == '-':
            self.data = int(nodes[self.left].data - nodes[self.right].data)
        elif self.op == '=':
            if nodes[self.left].data:
                self.data = nodes[self.left].data
            else:
                self.data = nodes[self.right].data
        else:
            raise NotImplemented("No such operation supported")
    
    def doReversedOpLeft(nodes, nodeName:str, op:str, val: int, left: int):
        if op == '*':
            nodes[nodeName].data = int(val / left)
        elif op == '/':
            nodes[nodeName].data = int(left / val)
        elif op == '+':
            nodes[nodeName].data = int(val - left)
        elif op == '-':
            nodes[nodeName].data = int(left - val)
        elif op == '=':
            nodes[nodeName].data = val
        else:
            raise NotImplemented("No such operation supported")
    def doReversedOpRight(nodes, nodeName:str, op:str, val: int, right: int):
        if op == '*':
            nodes[nodeName].data = int(val / right)
        elif op == '/':
            nodes[nodeName].data = int(val * right)
        elif op == '+':
            nodes[nodeName].data = int(val - right)
        elif op == '-':
            nodes[nodeName].data = int(val + right)
        elif op == '=':
            nodes[nodeName].data = val
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

def resolveEditedRoot(l):
    stack = deque()
    stack.append(l['root'])
    l['root'].op = '='
    l['humn'].data = None 

    while stack:
        head = stack[-1]
        if head.visited:
            if l[head.left].data and l[head.right].data:
                head.doOp(l)
            elif (l[head.left].data or l[head.right].data) and head == l['root']: 
                head.doOp(l)
            stack.pop()
        elif head.data or (not head.left and not head.right):
            stack.pop()
        else:
            stack.append(l[head.left])
            stack.append(l[head.right])
        head.visited = True
    
    # val = l['root'].data

    stack.append(l['root'])
    while stack:
        head = stack.pop()
        val = head.data
        if head.name == 'humn':
            break
        elif not l[head.left].data:
            Node.doReversedOpRight(l, l[head.left].name, head.op, val, l[head.right].data )
            stack.append(l[head.left])
        elif not l[head.right].data:
            Node.doReversedOpLeft(l, l[head.right].name, head.op, val, l[head.left].data )
            stack.append(l[head.right])
    
    return l['humn'].data

if __name__ == "__main__" :

    res: int = 0
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt'), 'r')
    lines = f.readlines()

    l = {}
    n = len(lines)
    for i in range(n):
        parts = lines[i].strip().split(' ')
        if len(parts) == 2:
            l[parts[0][:-1]] = Node(parts[0][:-1],int(parts[1]), None, None, None)
        elif len(parts) == 4:
            l[parts[0][:-1]] = Node(parts[0][:-1],None, parts[1], parts[3], parts[2])
        else:
            raise NotImplemented("No such input supported")

    print(resolveEditedRoot(l))
