import os

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def get_hamilton_distance(self, a):
        return max(abs(self.x - a.x), abs(self.y - a.y))


def move_tail(map, H: Point, T: Point):
    if H.x == T.x:
        # go down
        if H.y - T.y > 0:
            T.y = T.y + 1   
        else:
            T.y = T.y - 1
            
    elif H.y == T.y:
        # go down
        if H.x - T.x > 0:
            T.x = T.x + 1   
        else:
            T.x = T.x - 1
    else:
        if H.get_hamilton_distance(Point(T.x+1, T.y+1)) == 1:
            T.x = T.x + 1
            T.y = T.y + 1
        elif H.get_hamilton_distance(Point(T.x-1, T.y-1)) == 1:
            T.x = T.x - 1
            T.y = T.y - 1
        elif H.get_hamilton_distance(Point(T.x+1, T.y-1)) == 1:
            T.x = T.x + 1
            T.y = T.y - 1
        else:
            T.x = T.x - 1
            T.y = T.y + 1


    map[T.y][T.x] = 1
    pass

def move_in_map_u(steps: int, map, H: Point, T: Point):
    # H.y = H.y - 1
    step: int = 0
    while step < steps:
        step = step + 1
        H.y = H.y - 1
        if H.get_hamilton_distance(T) > 1:
            move_tail(map, H, T)
    pass
def move_in_map_d(steps: int, map, H: Point, T: Point):
    # H.y = H.y + 1
    step: int = 0
    while step < steps:
        step = step + 1
        H.y = H.y + 1
        if H.get_hamilton_distance(T) > 1:
            move_tail(map, H, T)
    pass

def move_in_map_l(steps: int, map, H: Point, T: Point):
    # H.x = H.x - 1
    step: int = 0
    while step < steps:
        step = step + 1
        H.x = H.x - 1
        if H.get_hamilton_distance(T) > 1:
            move_tail(map, H, T)
    pass

def move_in_map_r(steps: int, map, H: Point, T: Point):
    # H.x = H.x + 1
    step: int = 0
    while step < steps:
        step = step + 1
        H.x = H.x + 1
        if H.get_hamilton_distance(T) > 1:
            move_tail(map, H, T)
    pass

def get_result(map):
    res: int = 0
    for i in range(0,len(map)):
        for j in range(0, len(map[i])):
            if map[i][j] == 1:
                res += 1
    return res

def create_map(n: int):
    map = []
    for i in range(0,n):
        mapRow = []
        for j in range(0,n):
            mapRow.append(0)
        map.append(mapRow)
    return map

def move_in_map(dir, steps: int, map, H: Point, T: Point):
    if dir == 'U':
        move_in_map_u(steps, map, H, T)
    elif dir == 'D':
        move_in_map_d(steps, map, H, T)
    elif dir == 'L':
        move_in_map_l(steps, map, H, T)
    elif dir == 'R':
        move_in_map_r(steps, map, H, T)


if __name__ == "__main__" :
    
    n = 1000
    map = create_map(n)
    
    H:Point = Point(x=int(n/2),y=int(n/2))
    T:Point = Point(x=int(n/2),y=int(n/2))

    map[T.y][T.x] = 1

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input9.txt')) as fp:
        for line in fp:
            sl = line.split(' ')
            dir = sl[0]
            steps = int(sl[1])
            move_in_map(dir, steps, map, H, T)

        
    print(get_result(map))
