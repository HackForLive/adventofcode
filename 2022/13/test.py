import os
from collections import deque
from io import StringIO

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
    value: None

    def __init__(self, children, node_type: str):
        self.children = children
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
                root = Node([], "list")
                current = root
            else:
                tmp = Node([], "list")
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
            tmp = Node(children=num, node_type="item")
            current.Append(tmp)
            tmp.parent = current
        else:
            raise NotImplementedError("Cannot be parse %s" % i)
    return root

if __name__ == "__main__" :

    res: int = 0
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inputt.txt'), 'r')
    lines = f.readlines()

    for i in range(0, len(lines), 3):
        l = lines[i].strip()
        r = lines[i+1].strip()
        nl = get_node(l)
        nr = get_node(r)
        res += 1
        # if is_in_right_order(l,r):
            # res += int(i/3 + 1)
            #print(int(i/3 + 1))
        
    print(res)
    # 125 - too low
