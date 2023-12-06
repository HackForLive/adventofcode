import os
import pathlib
from typing import List

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


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
            else:
                print(lines[idl])
            idl = idl + 1
    # print(seeds)
    # print(seed_to_soil)
    # print(soil_to_fertilizer)
    # print(fertilizer_to_water)
    # print(water_to_light)
    # print(light_to_temperature)
    # print(temperature_to_humidity)
    # print(humidity_to_location)

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


def map_seed(seed: int, s_map: List[List[int]]):
    res = seed
    # print(f"seed before {res}")
    for s_m in s_map:
        if seed >= s_m[1] and s_m[1]+s_m[2]-1 >= seed:
            res = s_m[0] + (seed - s_m[1])
            break
    # print(f"seed after {res}")
    return res


# @timer_decorator
def solve_1():
    parse()

if __name__ == '__main__':
    solve_1()
