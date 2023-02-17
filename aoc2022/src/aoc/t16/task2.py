import os
import numpy as np


def recursive(time: int, vertex1: str, vertex2: str, visited: int):
    # time is out
    if time <= 0:
        return 0
    
    # cached
    if dp[time][v_number[vertex1]][v_number[vertex2]][visited] > -1:
        return dp[time][v_number[vertex1]][v_number[vertex2]][visited]

    ## both open
    ## 1. open and 2. go
    ## 1. go and 2. open
    ## both go

    maximum: int = 0
    # both open
    if v_val[vertex1] > 0 and (visited & v_bitflag[vertex1]) == 0 and \
       v_val[vertex2] > 0 and (visited & v_bitflag[vertex2]) == 0 and \
       vertex1 != vertex2:
        maximum = max(recursive(time=time-1, vertex1=vertex1, vertex2=vertex2, 
        visited=(visited | v_bitflag[vertex1] | v_bitflag[vertex2])) + 
        v_val[vertex1]*(time-1) + v_val[vertex2]*(time-1) , maximum)

    if v_val[vertex1] > 0 and (visited & v_bitflag[vertex1]) == 0:
        for surrouding in v[vertex2]:
            maximum = max(recursive(time=time-1, vertex1=vertex1, vertex2=surrouding, 
            visited=(visited | v_bitflag[vertex1])) + v_val[vertex1]*(time-1), maximum)
    
    if v_val[vertex2] > 0 and (visited & v_bitflag[vertex2]) == 0:
        for surrouding in v[vertex1]:
            maximum = max(recursive(time=time-1, vertex1=surrouding, vertex2=vertex2, 
            visited=(visited | v_bitflag[vertex2])) + v_val[vertex2]*(time-1), maximum)
    
    # both go
    for surrouding1 in v[vertex1]:
        for surrouding2 in v[vertex2]:
            maximum = max(recursive(time=time-1, vertex1=surrouding1, vertex2=surrouding2, visited=visited), maximum)

    dp[time][v_number[vertex1]][v_number[vertex2]][visited] = maximum
    return maximum


if __name__ == "__main__" :
    v = {}
    v_bitflag = {}
    v_number = {}
    v_val = {}
    T_time: int = 26
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
    dp = np.full((T_time + offset , len(v) +  offset, len(v) +  offset, 2**(len(v_filtered)) + offset), -1, dtype=np.int16)
    
    res = recursive(time=T_time, vertex1=V_start, vertex2=V_start, visited=0)
    print(res)
