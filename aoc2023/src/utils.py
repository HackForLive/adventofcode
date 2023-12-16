def get_direction(direction: str):
    """
    Get y,x list based on direction
    """
    directions = {
        "N": [-1,0],
        "S": [1,0],
        "W": [0,-1],
        "E": [0,1]
    }

    return directions[direction]

def get_direction_val(direction: str):
    directions = {
        "N": 3,
        "S": 1,
        "W": 2,
        "E": 0
    }

    return directions[direction]

def get_next_left_dir(direction: str):
    """
    Turn 90 degrees in counter clockwise manner 
    """
    directions = {
        "N": 0,
        "W": 1,
        "S": 2,
        "E": 3
    }
    directions_reversed = dict((v, k) for k, v in directions.items())

    numb = (directions[direction] + 1) % len(directions)
    return directions_reversed[numb]

def get_next_right_dir(direction: str):
    """
    Turn 90 degrees in clockwise manner 
    """
    directions = {
        "N": 0,
        "E": 1,
        "S": 2,
        "W": 3
    }
    directions_reversed = dict((v, k) for k, v in directions.items())

    numb = (directions[direction] + 1) % len(directions)
    return directions_reversed[numb]
