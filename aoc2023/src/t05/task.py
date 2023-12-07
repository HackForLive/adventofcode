import os
import pathlib
from typing import List

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'input_test.txt')


def parse():
    seeds = []
    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []

    with open(input_file, 'r', encoding='utf8') as f:
        lines = f.readlines()

        idl = 0
        while idl < len(lines):
            if 'seeds:' in lines[idl]:
                seeds = [int(n.strip()) for n in lines[idl].split(' ')[1:]]
            elif 'seed-to-soil map:' in lines[idl]:
                idl = idl + 1
                while lines[idl].strip() != '':
                    seed_to_soil.append([int(n.strip()) for n in lines[idl].split(' ')])
                    idl = idl + 1
            elif 'soil-to-fertilizer' in lines[idl]:
                idl = idl + 1
                while lines[idl].strip() != '':
                    soil_to_fertilizer.append([int(n.strip()) for n in lines[idl].split(' ')])
                    idl = idl + 1
            elif 'fertilizer-to-water map:' in lines[idl]:
                idl = idl + 1
                while lines[idl].strip() != '':
                    fertilizer_to_water.append([int(n.strip()) for n in lines[idl].split(' ')])
                    idl = idl + 1
            elif 'water-to-light map:' in lines[idl]:
                idl = idl + 1
                while lines[idl].strip() != '':
                    water_to_light.append([int(n.strip()) for n in lines[idl].split(' ')])
                    idl = idl + 1
            elif 'light-to-temperature map:' in lines[idl]:
                idl = idl + 1
                while lines[idl].strip() != '':
                    light_to_temperature.append([int(n.strip()) for n in lines[idl].split(' ')])
                    idl = idl + 1
            elif 'temperature-to-humidity map:' in lines[idl]:
                idl = idl + 1
                while lines[idl].strip() != '':
                    temperature_to_humidity.append([int(n.strip()) for n in lines[idl].split(' ')])
                    idl = idl + 1
            elif 'humidity-to-location map:' in lines[idl]:
                idl = idl + 1
                while idl < len(lines) and lines[idl].strip() != '':
                    humidity_to_location.append([int(n.strip()) for n in lines[idl].split(' ')])
                    idl = idl + 1
            idl = idl + 1

    return (seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, 
            light_to_temperature, temperature_to_humidity, humidity_to_location)
    # print(seeds)
    # print(seed_to_soil)
    # print(soil_to_fertilizer)
    # print(fertilizer_to_water)
    # print(water_to_light)
    # print(light_to_temperature)
    # print(temperature_to_humidity)
    # print(humidity_to_location)


def map_seed(seed: int, s_map: List[List[int]]):
    res = seed
    # print(f"seed before {res}")
    for s_m in s_map:
        if s_m[1] <= seed <= s_m[1]+s_m[2]-1:
            res = s_m[0] + (seed - s_m[1])
            break
    # print(f"seed after {res}")
    return res

def map_reverse_seed(seed: int, s_map: List[List[int]]):
    res = seed
    # print(f"seed before {res}")
    for s_m in s_map:
        if s_m[0] <= seed <= s_m[0]+s_m[2]-1:
            res = s_m[1] + (seed - s_m[0])
            break
    # print(f"seed after {res}")
    return res


# @timer_decorator
def solve_1():
    (seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light,
            light_to_temperature, temperature_to_humidity, humidity_to_location) = parse()
    res_seed = []
    for seed in seeds:
        seed = map_seed(seed=seed, s_map=seed_to_soil)
        seed = map_seed(seed=seed, s_map=soil_to_fertilizer)
        seed = map_seed(seed=seed, s_map=fertilizer_to_water)
        seed = map_seed(seed=seed, s_map=water_to_light)
        seed = map_seed(seed=seed, s_map=light_to_temperature)
        seed = map_seed(seed=seed, s_map=temperature_to_humidity)
        seed = map_seed(seed=seed, s_map=humidity_to_location)
        res_seed.append(seed)
    print(min(res_seed))

def solve_2_reverse():
    (seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light,
            light_to_temperature, temperature_to_humidity, humidity_to_location) = parse()
    seeds_2 = [range(seeds[step], seeds[step] + seeds[step+1], 1)
               for step in list(range(0, len(seeds), 2))]

    stop_n = 1
    found: bool = False

    for _ in range(0,3000000000, 1):
        seed = stop_n
        seed = map_reverse_seed(seed=seed, s_map=humidity_to_location)
        seed = map_reverse_seed(seed=seed, s_map=temperature_to_humidity)
        seed = map_reverse_seed(seed=seed, s_map=light_to_temperature)
        seed = map_reverse_seed(seed=seed, s_map=water_to_light)
        seed = map_reverse_seed(seed=seed, s_map=fertilizer_to_water)
        seed = map_reverse_seed(seed=seed, s_map=soil_to_fertilizer)
        seed = map_reverse_seed(seed=seed, s_map=seed_to_soil)

        # is in seeds range?
        for s in seeds_2:
            if seed in s:
                found = True
                break
        if found:
            break
        stop_n = stop_n+ 1
    print(stop_n)
    print(found)
    # quick cheat - 100165128
    
    # stop_n = 529830500
    # initial_s = 0
    # for i in range(stop_n, 129000000, -100):
    #     seed = i
    #     seed = map_seed(seed=seed, s_map=seed_to_soil)
    #     seed = map_seed(seed=seed, s_map=soil_to_fertilizer)
    #     seed = map_seed(seed=seed, s_map=fertilizer_to_water)
    #     seed = map_seed(seed=seed, s_map=water_to_light)
    #     seed = map_seed(seed=seed, s_map=light_to_temperature)
    #     seed = map_seed(seed=seed, s_map=temperature_to_humidity)
    #     seed = map_seed(seed=seed, s_map=humidity_to_location)
    #     if seed < stop_n:
    #         stop_n = seed
    #         initial_s = i
    # print(stop_n)
    # print(initial_s)
    
    # 303 is too low

def solve_2():
    (seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light,
            light_to_temperature, temperature_to_humidity, humidity_to_location) = parse()
    seeds_2 = [range(seeds[step], seeds[step] + seeds[step+1], 1)
               for step in list(range(0, len(seeds), 2))]

    # print(seeds_2)
    for map_s in (
        seed_to_soil,
        soil_to_fertilizer,
        fertilizer_to_water,
        water_to_light,
        light_to_temperature, 
        temperature_to_humidity,
        humidity_to_location
            ):
        n = len(seeds_2)
        # for i in range(n):
            # print(i)
            # seeds_2.extend(map_seed_interval(seed_r=seeds_2[i], s_map=map_s))
        # print(seeds_2)
    # for seed in range(len(seeds_2)):
    #     seeds_2.extend(map_seed_interval(seed_r=seed, s_map=soil_to_fertilizer))
    # for seed in range(len(seeds_2)):
    #     seeds_2.extend(map_seed_interval(seed_r=seed, s_map=soil_to_fertilizer))


    print(min([seed_i.start for seed_i in seeds_2]))

def map_seed_intervals(seed_r: range, s_map: List[List[int]]):
    start = seed_r.start
    stop = seed_r.stop

    res: List[range] = [seed_r]
    for s_m in s_map:
        for r in res:
            tmp = map_seed_interval(seed_r=seed_r, s_m=s_m)
        res.extend
    return res


def map_seed_interval(seed_r: range, s_m: List[int]) -> List[range]:
    start = seed_r.start
    stop = seed_r.stop

    res: List[range] = []
    n_start = -1
    n_stop = -1

    if s_m[1] <= start <= s_m[1]+s_m[2]-1:
        if stop > s_m[1]+s_m[2]-1:
            n_stop = s_m[1]+s_m[2]-1
            n_stop = s_m[0] + (n_stop - s_m[1])
            n_start = s_m[0] + (start - s_m[1])

            if range(s_m[1]+s_m[2], stop):
                res.append(range(s_m[1]+s_m[2], stop))

            res.append(range(n_start, n_stop))
        else:
            n_stop = s_m[0] + (stop - s_m[1])
            n_start = s_m[0] + (start - s_m[1])
            res.append(range(n_start, n_stop))
    elif s_m[1] <= stop <= s_m[1]+s_m[2]-1:
        if start < s_m[1]:
            n_start = s_m[1]
            n_start = s_m[0] + (n_start - s_m[1])
            n_stop = s_m[0] + (stop - s_m[1])

            if range(start, s_m[1]):
                res.append(range(start, s_m[1]))

            res.append(range(n_start, n_stop))
        else:
            n_start = s_m[0] + (start - s_m[1])
            n_stop = s_m[0] + (stop - s_m[1])
            res.append(range(n_start, n_stop))

    # res.append(seed_r)
    return res


if __name__ == '__main__':
    solve_1()
    solve_2()
    # solve_2_reverse()
