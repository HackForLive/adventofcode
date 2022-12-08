import os

def is_visible_from_top(row, col, map):
    curr: int = row - 1
    while curr >= 0:
        if map[row][col] <= map[curr][col]:
            return False
        curr -= 1
    return True
def is_visible_from_bottom(row, col, map):
    curr: int = row + 1
    while curr < len(map):
        if map[row][col] <= map[curr][col]:
            return False
        curr += 1
    return True
def is_visible_from_left(row, col, map):
    curr: int = col - 1
    while curr >= 0:
        if map[row][col] <= map[row][curr]:
            return False
        curr -= 1
    return True
def is_visible_from_right(row, col, map):
    curr: int = col + 1
    while curr < len(map[row]):
        if map[row][col] <= map[row][curr]:
            return False
        curr += 1
    return True

def is_visible(row, col, map):
    if is_visible_from_top(row, col, map): return True
    if is_visible_from_bottom(row, col, map): return True
    if is_visible_from_left(row, col, map): return True
    if is_visible_from_right(row, col, map): return True
    return False

def get_score_from_t(row, col, map):
    curr: int = row - 1
    score: int = 0
    while curr >= 0:
        score += 1
        if map[row][col] <= map[curr][col]:
            break
        curr -= 1
    return score
def get_score_from_b(row, col, map):
    curr: int = row + 1
    score: int = 0
    while curr < len(map):
        score += 1
        if map[row][col] <= map[curr][col]:
            break
        curr += 1
    return score
def get_score_from_l(row, col, map):
    curr: int = col - 1
    score: int = 0
    while curr >= 0:
        score += 1
        if map[row][col] <= map[row][curr]:
            break
        curr -= 1
    return score
def get_score_from_r(row, col, map):
    curr: int = col + 1
    score: int = 0
    while curr < len(map[row]):
        score += 1
        if map[row][col] <= map[row][curr]:
            break
        curr += 1
    return score


def get_scenic_score(row, col, map):
    return get_score_from_b(row, col, map) * get_score_from_l(row, col, map) * \
    get_score_from_r(row, col= col, map= map) * get_score_from_t(row, col, map)

def get_result(map):
    res: int = 0
    for i in range(0,len(map)):
        for j in range(0, len(map[i])):
            if is_visible(i, j, map): 
                res = res + 1
    return res

def get_result2(map):
    res: int = 0
    for i in range(0,len(map)):
        for j in range(0, len(map[i])):
            scenic_score = get_scenic_score(i, j, map)
            if scenic_score > res: 
                res = scenic_score
    return res

if __name__ == "__main__" :
    map = []
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt')) as fp:
        for line in fp:
            l = line.strip()
            mapRow = []
            for n in l:
                mapRow.append(int(n))
            map.append(mapRow)
    print(get_result2(map))
