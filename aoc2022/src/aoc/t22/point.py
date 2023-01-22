"""Module provides Node class."""

class Node:
    """
    Class representing Node with direction information
    """
    def __init__(self, x: int, y: int, direction: str):
        self.x = x
        self.y = y
        self.direction = direction

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
            getattr(other, 'x', None) == self.x and
            getattr(other, 'y', None) == self.y and
            getattr(other, 'direction', None) == self.direction)

    def __hash__(self):
        return hash(str(self.x) + str(self.y) + self.direction)
