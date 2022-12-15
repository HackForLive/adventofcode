import os
from collections import deque
from io import StringIO
import functools
import copy

class StringBuilder:
     _file_str = None

     def __init__(self):
         self._file_str = StringIO()
     def Append(self, str):
         self._file_str.write(str)
     def __str__(self):
         return self._file_str.getvalue()

class Node:
    parent = None
    children = []
    node_type = ''
    height: int = None
    value: None

    def __init__(self, children, height: int, node_type: str):
        self.children = children
        self.height = height
        self.node_type = node_type

    def Append(self, node):
        self.children.append(node)

    def get_size(self):
        return len(self.children)

    def is_list_type(self):
        return self.node_type == 'list'
    
    def is_item_type(self):
        return self.node_type == 'item'

def get_node(line: str):
    # stack = deque()
    root: Node = None
    current: Node = None
    for i in range(0, len(line)):
        # create node

        if line[i] == '[':
            if not root:
                root = Node([],1, "list")
                current = root
            else:
                tmp = Node([],current.height + 1, "list")
                current.children.append(tmp)
                tmp.parent = current
                current = tmp
        # go up
        elif line[i] == ']':
            if current.parent:
                current = current.parent
        # next item
        elif line[i] == ',':
            continue
        elif line[i].isdigit():
            sb = StringBuilder()
            sb.Append(line[i])
            j: int = i + 1
            while j < len(line) and line[j].isdigit():
                sb.Append(line[j])
                j += 1
            num = int(str(sb))
            tmp = Node(children=num, height=current.height + 1, node_type="item")
            current.Append(tmp)
            tmp.parent = current
        else:
            raise NotImplementedError("Cannot be parse %s" % i)
    return root

def compare_leaf_nodes(left: Node, right: Node):
    if left.children < right.children:
        return 1
    elif left.children > right.children:
        return -1
    return 0

def compare_nodes(left: Node, right: Node):
    lstack = deque()
    rstack = deque()

    lstack.append(copy.deepcopy(left))
    rstack.append(copy.deepcopy(right))

    while True:
        if rstack and not lstack:
            return 1
        if lstack and not rstack:
            return -1
        if not lstack and not rstack:
            return 0
        
        l = lstack.pop()
        r = rstack.pop()

        # control height
        if l.height > r.height:
            return -1
        
        if l.height < r.height:
            return 1

        # check two values
        if l.is_item_type() and r.is_item_type():
            if compare_leaf_nodes(l,r) == 1:
                return 1
            elif compare_leaf_nodes(l,r) == -1:
                return -1
            else:
                continue
        elif l.is_item_type():
            # create new list from value
            new = Node(children=l.children, height=l.height + 1, node_type="item")
            new.parent = l
            l.children = [new]
            l.node_type = "list"
            lstack.append(l)
            rstack.append(r)
        elif r.is_item_type():
             # create new list from value
            new = Node(children=r.children, height=r.height + 1, node_type="item")
            new.parent = r
            r.children = [new]
            r.node_type = "list"
            lstack.append(l)
            rstack.append(r)
        else:
            # dig deeper
            for i in reversed(range(len(l.children))):
                lstack.append(l.children[i])
            for i in reversed(range(len(r.children))):
                rstack.append(r.children[i])

def find_node(nodes, node: Node):
    for i in range(len(nodes)):
        if compare_nodes(nodes[i], node) == 0:
            return i
    return -1

if __name__ == "__main__" :

    res: int = 0
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt'), 'r')
    lines = f.readlines()

    nodes = []
    for i in range(len(lines)):
        l = lines[i].strip()
        if len(l) == 0:
            continue
        node = get_node(l)
        nodes.append(node)
        # if compare_nodes(nl, nr):
        #     print(int(i/3 + 1))
        #     res += int(i/3 + 1)
    nodes.append(get_node('[[2]]'))
    nodes.append(get_node('[[6]]'))

    sortedn = sorted(nodes, key=functools.cmp_to_key(compare_nodes), reverse=True)

    a: int = find_node(sortedn, get_node('[[2]]')) + 1
    b: int = find_node(sortedn, get_node('[[6]]')) + 1

    print(a)
    print(b)
    print(a*b)