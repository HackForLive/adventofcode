import os
from queue import PriorityQueue

q = PriorityQueue()
cal = 0
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input1.txt')) as fp:
    for line in fp:
        row = line.strip()
        if row == "":
            q.put(-cal)
            cal = 0
        else:
            cal = int(row) + cal
        
print(-(q.get() + q.get() + q.get()))
