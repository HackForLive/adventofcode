from enum import Enum


class Direction(Enum):
    """
    N/S/E/W
    """
    NORTH = [-1, 0]
    EAST = [0, 1]
    SOUTH = [1, 0]
    WEST = [0, -1]

    @classmethod
    def get_name_by_value(cls,val):
        return { v:k for k,v in dict(vars(cls)).items() if isinstance(v,list)}.get(val, None)


def get_next_left_dir(direction: Direction):
    """
    Turn 90 degrees in counter clockwise manner 
    """
    directions = {
        Direction.NORTH: Direction.WEST,
        Direction.WEST: Direction.SOUTH,
        Direction.SOUTH: Direction.EAST,
        Direction.EAST: Direction.NORTH
    }
    return directions[direction]

def get_next_right_dir(direction: Direction):
    """
    Turn 90 degrees in clockwise manner 
    """
    directions = {
        Direction.NORTH: Direction.EAST,
        Direction.EAST: Direction.SOUTH,
        Direction.SOUTH: Direction.WEST,
        Direction.WEST: Direction.NORTH
    }
    return directions[direction]
