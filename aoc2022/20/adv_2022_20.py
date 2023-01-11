import os

class Node:
    def __init__(self, data: int, order: int):
        self.data = data
        self.order = order

def shuffle(numbers):
    n = len(numbers)
    i = 0
    while i < n:
        currNode = next((x for x in numbers if x.order == i), None)
        j = numbers.index(currNode)
        numbers.pop(j)
        numbers.insert((j + currNode.data)%(n-1), currNode)
        i += 1

def shuffleNTimes(numbers, times: int):
    t = 0
    print("----------")
    while t < times:
        shuffle(numbers)
        t += 1
        print(list(map(lambda x: x.data, numbers)))
    print("----------")


if __name__ == "__main__" :

    res: int = 0
    dec_key: int = 811589153
    times: int = 10
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt'), 'r')
    lines = f.readlines()

    l = []
    n = len(lines)
    for i in range(n):
        node = Node(int(lines[i].strip()), i)
        node.data = node.data * dec_key
        l.append(node)

    print(list(map(lambda x: x.data, l)))

    shuffleNTimes(l, times=times)

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

    print("res: %d" % (f+s+t))
