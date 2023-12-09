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
    for s_m in s_map:
        if s_m[1] <= seed <= s_m[1]+s_m[2]-1:
            res = s_m[0] + (seed - s_m[1])
            break
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


def sort_and_merge_intervals(intervals: List[range]):
    res = []
    s_ints = sorted(intervals, key=lambda x: x.start)
    for s in range(1, len(s_ints)):
        if s_ints[s-1].start == s_ints[s].start and s_ints[s-1].stop == s_ints[s].stop:
            res.append(range(s_ints[s].start, s_ints[s].stop))
        elif s_ints[s-1].stop > s_ints[s].start:
            res.append(range(s_ints[s-1].start, max(s_ints[s-1].stop, s_ints[s].stop)))
        else:
            res.append(range(s_ints[s-1].start, s_ints[s-1].stop))
            if s == len(s_ints) - 1:
                res.append(range(s_ints[s].start, s_ints[s].stop))
    return res

def apply_mapping(dest: range, source: range, orig_r: range) -> List[range]:

    diff = source.start - dest.start
    # outside
    if source.stop <= orig_r.start or source.start >= orig_r.stop:
        # just return the original
        return [orig_r]
    # inside orig
    elif source.start < orig_r.start and source.stop > orig_r.stop:
        # three intervals
        return [range(orig_r.start - diff, orig_r.stop - diff)]
    # insde source
    elif orig_r.start < source.start and orig_r.stop > source.stop:
        return [
            range(source.start, orig_r.start - 1),
            range(orig_r.start - diff, orig_r.stop - diff),
            range(orig_r.stop + 1, source.stop)]
    # left
    elif source.start < orig_r.stop <= source.stop and orig_r.start <= source.start:
        return [
            range(orig_r.start, source.start - 1),
            range(source.start - diff, orig_r.stop - diff)
            ]
    # right
    elif source.stop > orig_r.start >= source.start and orig_r.stop >= source.stop:
        return [
            range(orig_r.start - diff, source.stop - diff),
            range(source.stop - diff + 1, orig_r.stop)
            ]
    else:
        # print(source)
        # print(orig_r)
        raise ValueError('What???')

def get_mapping_range_from_mapping(mapping: List[int]) -> (range, range):
    # print(mapping)
    return range(mapping[0], mapping[0] + mapping[2]), range(mapping[1], mapping[1] + mapping[2])

def find_range_and_apply_mapping(intervals: List[range], mapping: List[int]):

    m_dest, m_source = get_mapping_range_from_mapping(mapping=mapping)
    res: List[range] = []
    for i in range(0, len(intervals), 1):
        if intervals[i].stop < m_source.start or intervals[i].start > m_source.stop:
            res.append(intervals[i])
        # do mapping
        else:
            res.extend(apply_mapping(source=m_source, dest=m_dest, orig_r=intervals[i]))
    return res


def solve_2():
    (seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light,
            light_to_temperature, temperature_to_humidity, humidity_to_location) = parse()
    seeds_2 = [range(seeds[step], seeds[step] + seeds[step+1], 1)
               for step in list(range(0, len(seeds), 2))]

    # print(seeds_2)
    seeds_2 = sort_and_merge_intervals(seeds_2)
    print(seeds_2)
    for map_s in (
        seed_to_soil,
        soil_to_fertilizer,
        fertilizer_to_water,
        water_to_light,
        light_to_temperature, 
        temperature_to_humidity,
        humidity_to_location
            ):
        print(f"{map_s =}")
        for m_s in map_s:
            print(f"{m_s =}")
            seeds_2 = find_range_and_apply_mapping(intervals=seeds_2, mapping=m_s)
            print(f"{seeds_2 =}")
            seeds_2 = sort_and_merge_intervals(seeds_2)
        break
        # break
    print(seeds_2[:50])

    print(sorted(seeds_2, key=lambda x: x.start)[0].start)

if __name__ == '__main__':
    solve_1()
    solve_2()
    # solve_2_reverse()
