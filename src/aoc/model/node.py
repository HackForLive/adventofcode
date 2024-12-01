from attr import define
from aoc.model.direction import Direction

@define
class Node:
    """
    Current Node
    """
    x: int
    y: int
    direction: Direction

    def __eq__(self, obj):
        return isinstance(obj, Node) and (obj.x == self.x
                                               and obj.y == self.y
                                               and obj.direction == self.direction)

    def __hash__(self):
        return hash((self.x, self.y))