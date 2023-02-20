import os
import numpy as np

# TODO: optimaze
def get_max_geodes(time, ore, clay, obs, ore_n, clay_n, obs_n):
    # time is out
    if time <= 0 or dp.shape[4] <= ore_n or dp.shape[5] <= clay_n or dp.shape[6] <= obs_n:
        return 0
    
    # cached
    if dp[time][ore][clay][obs][ore_n][clay_n][obs_n] > -1:
        return dp[time][ore][clay][obs][ore_n][clay_n][obs_n]
    
    maximum: int = 0
    # try to build robot

    if  costs['geo'][0] <= ore_n and costs['geo'][1] <= obs_n:
        maximum = max(
            get_max_geodes(time-1, ore, clay, obs, ore_n+ore-costs['geo'][0], clay_n+clay, obs_n+obs-costs['geo'][1]) + time - 1, 
            maximum)
    
    if dp.shape[3] > obs + 1 and  costs['obs'][0] <= ore_n and costs['obs'][1] <= clay_n:
        maximum = max(
            get_max_geodes(time-1, ore, clay, obs+1, ore_n+ore-costs['obs'][0], clay_n+clay-costs['obs'][1], obs_n+obs), 
            maximum)
    if dp.shape[2] > clay + 1 and costs['clay'][0] <= ore_n:
        maximum = max(
            get_max_geodes(time-1, ore, clay+1, obs, ore_n+ore-costs['clay'][0], clay_n+clay, obs_n+obs), maximum)
    
    if dp.shape[1] > ore + 1 and costs['ore'][0] <= ore_n:
        maximum = max(
            get_max_geodes(time-1, ore+1, clay, obs, ore_n+ore-costs['ore'][0], clay_n+clay, obs_n+obs), maximum)
        
    maximum = max(get_max_geodes(time-1, ore, clay, obs, ore_n+ore, clay_n+clay, obs_n+obs), maximum)

    dp[time][ore][clay][obs][ore_n][clay_n][obs_n] = maximum
    return maximum

if __name__ == "__main__" :
    v = {}
    v_bitflag = {}
    v_number = {}
    v_val = {}
    T_time: int = 24

    result = 0

    with open(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inputt.txt'), mode='r', encoding="UTF8") as f:
        for idx, line in enumerate(f):
            id_bp = int(line.split(':')[0].split(' ')[-1].strip())
            ore_cost = int(line.split(':')[1].split('.')[0].split('costs')[1].split(' ')[1].strip())
            clay_cost = int(line.split(':')[1].split('.')[1].split('costs')[1].split(' ')[1].strip())

            obs_cost = int(line.split(':')[1].split('.')[2].split('costs')[1].split(' ')[1].strip())
            obs2_cost = int(line.split(':')[1].split('.')[2].split('costs')[1].split(' ')[4].strip())

            geo_cost = int(line.split(':')[1].split('.')[3].split('costs')[1].split(' ')[1].strip())
            geo2_cost = int(line.split(':')[1].split('.')[3].split('costs')[1].split(' ')[4].strip())

            costs = {
                'ore': [ore_cost],
                'clay': [clay_cost],
                'obs': [obs_cost, obs2_cost],
                'geo': [geo_cost, geo2_cost]
            }

            offset = 1
            max_ore_r = int(max(clay_cost, max(obs_cost, geo_cost)))
            max_clay_r = int(obs2_cost)
            max_obs_r = int(obs2_cost)

            # TODO: should be optimazed
            dp = np.full(
                (
                T_time + offset,
                max_ore_r + offset, 
                max_clay_r + offset,
                max_obs_r + offset,
                max_ore_r*3,
                max_clay_r*3,
                max_obs_r*3
                ), -1, dtype=np.int8)

            # print(f"{dp.shape[0] = }")
            # print(f"{dp.shape[1] = }")
            # print(f"{dp.shape[2] = }")

            res = get_max_geodes(T_time, 1, 0, 0, 0, 0, 0)
            print(f"id: {id_bp =} res:{res = }")
            result = result + id_bp * res
    print(result)
