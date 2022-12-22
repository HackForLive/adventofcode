import os

class Node:
    __isProcessed: bool = None
    def __init__(self, data):
        self.data = data
        self.__isProcessed = False

    def doProcess(self):
        self.__isProcessed = True
    
    def isProcessed(self):
        return self.__isProcessed

if __name__ == "__main__" :

    res: int = 0
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt'), 'r')
    lines = f.readlines()

    l = []
    n = len(lines)
    for i in range(n):
        node = Node(int(lines[i].strip()))
        l.append(node)

    i = 0
    while i < n:
        currNode: Node = l[i]
        if currNode.isProcessed():
            i += 1
            # print('processed')
            # print("value: %s" % (currNode.data))
            # print(list(map(lambda x: x.data, l)))
            continue        
        # print('unprocessed')
        # print('index %d' % (i))
        # print("node value: %s" % (currNode.data))
        l.pop(i)
        if (i + currNode.data)%(n-1) == 0:
            l.append(currNode)
            # print('insert at: %d' % ((i + currNode.data)))
            # l.insert((i + currNode.data)%n, currNode)
        else:
            # print('insert at: %d' % ((i + currNode.data)))
            l.insert((i + currNode.data)%(n-1), currNode)
        # print(list(map(lambda x: x.data, l)))
        currNode.doProcess()
        i = 0

    start = 0
    print(list(map(lambda x: x.data, l)))
    for i in range(len(l)):
        if l[i].data == 0:
            start = i
            print(i)
            break
    
    f = l[(1000+start)%n].data
    s = l[(2000+start)%n].data
    t = l[(3000+start)%n].data

    print(f)
    print(s)
    print(t)

    # 10444 too high
    # -2662
    print("res: %d" % (f+s+t))

# [1, 2, -3, 4, 0, 3, -2]
# 4
# 4
# -3
# 2
# res: 3