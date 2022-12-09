import os
from collections import deque  

# Represents a node of an n-ary tree
class Node :

    def __init__(self, name: str, value: int, parent):
        self.name = name
        self.value = value
        self.parent = parent
        self.children = []
    
    def add_child(self, obj):
        self.children.append(obj)

def get_result(node: Node):
    res:int = 0
    
    q = deque()
    q.append(node)

    while q:
        curr:Node = q.pop()
        unresolved = list(filter(lambda x: x.value == -1, curr.children))
        resolved = list(filter(lambda x: x.value != -1, curr.children))

        if not unresolved:
            curr.value = sum(c.value for c in resolved)
            if curr.value <= 100000:
                res += curr.value
        else:
            q.append(curr)
            for i in unresolved:
                q.append(i)
    return res

def get_root():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input7.txt')) as fp:
        root: Node = None
        curr: Node = None
        for line in fp:
            lstripped = line.strip()

            # command
            if lstripped.startswith("$"):
                action = lstripped.split(" ")[1].strip()
                # list
                if action == "ls":
                    continue
                elif action == "cd":
                    name = lstripped.split(" ")[2].strip()
                    # goup
                    if name == "..":
                        curr = curr.parent
                    # name
                    elif name == "/":
                        root = Node(name=name, value=-1, parent=None)
                        curr = root
                    else:
                        to = list(filter(lambda x: x.name == name, curr.children))[0]
                        curr = to

            # directory
            elif lstripped.startswith("dir"):
                name = lstripped.split(" ")[1].strip()
                node = Node(name=name, value=-1, parent=curr)
                curr.add_child(node)
            # file
            else:
                value = int(lstripped.split(" ")[0].strip())
                name = lstripped.split(" ")[1].strip()
                node = Node(name=name, value=value, parent=curr)
                curr.add_child(node)
        return root

if __name__ == "__main__" :
    root: Node = get_root()
    print(get_result(root))
