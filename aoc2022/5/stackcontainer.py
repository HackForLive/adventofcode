from collections import deque

class StackContainer:
  def __init__(self, stackCount):
    self.stacks = []
    for stack in range(0, stackCount, 1):
        self.stacks.append(deque())

  def add_item_to_stack(self, id, item):
    self.stacks[id].append(item)

  def reverse_stacks(self):
    for i in range(0, len(self.stacks)):
        self.stacks[i].reverse()

  def move_items(self, srcStack, destStack, itemCount):
    for stack in range(0, itemCount, 1):
        self.stacks[destStack-1].append(self.stacks[srcStack-1].pop())
  
  def move_items_with_same_order(self, srcStack, destStack, itemCount):
    tmp = deque()
    for stack in range(0, itemCount, 1):
      tmp.append(self.stacks[srcStack-1].pop())
    while tmp:                # Loop until empty
      self.stacks[destStack-1].append(tmp.pop())