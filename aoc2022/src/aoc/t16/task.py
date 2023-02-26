import os
import numpy as np


def recursive(time: int, vertex: str, visited: int):
    # time is out
    if time <= 0:
        return 0
    
    # cached
    if dp[time][v_number[vertex]][visited] > -1:
        return dp[time][v_number[vertex]][visited]

    maximum: int = 0
    # flow > 0 and not visited, we can potentionally open
    if v_val[vertex] > 0 and (visited & v_bitflag[vertex]) == 0:
        maximum = max(recursive(time=time-1, vertex=vertex, visited=(visited | v_bitflag[vertex])) + v_val[vertex]*(time-1), maximum)
    for surrouding in v[vertex]:
        maximum = max(recursive(time=time-1, vertex=surrouding, visited=visited), maximum)

    dp[time][v_number[vertex]][visited] = maximum
    return maximum


if __name__ == "__main__" :
    v = {}
    v_bitflag = {}
    v_number = {}
    v_val = {}
    T_time: int = 30
    V_start: str = "AA" 

    with open(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inputt.txt'), mode='r', encoding="UTF8") as f:
        for idx, line in enumerate(f):
            name = line.split(';')[0].split(' ')[1].strip()
            v_val[name] = int(line.split(';')[0].split(' ')[-1].split('=')[-1].strip())
            v[name] = [x.strip() for x in line.split(';')[1].split('valves')[-1].split('valve')[-1].split(',')]
            v_number[name] = idx
    
    v_filtered = {k:v for (k,v) in v.items() if v_val[k] > 0}

    for idx, key in enumerate(v_filtered):
        v_bitflag[key] = 1 << idx

    offset = 2
    dp = np.full((T_time + offset , len(v) +  offset, 2**(len(v_filtered)) + offset), -1, dtype=np.int16)
    
    res = recursive(T_time, V_start, 0)
    print(res)
