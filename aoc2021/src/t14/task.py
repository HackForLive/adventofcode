import os
import pathlib
# from line_profiler import LineProfiler

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


def map_char_to_range(c: str) -> int:
    """
    Map 'A'-'Z' to 0-25 
    """
    return ord(c) - ord('A')


def from_range_n_get_char(n: int) -> str:
    """
    Map 0-25 to 'A'-'Z'
    """
    # 65 - A
    return chr(n + 65)


#[26x26] x steps x 26
# a,b => [a,b]
# a,b,c => [a,b] + [b,c] - b

def solve_2(steps: int = 1):
    with open(input_file, 'r', encoding='utf8') as f:
        # 'A' => 65, map to 0-25

        template_s = list(f.readline().strip())
        map_dic = {line.strip().split(' -> ')[0]:line.strip().split(' -> ')[1]
               for line in f if line.strip() != ''}

        memo_cache = np.zeros(shape=(26,26,steps+1,26), dtype=np.uint64)

        for step in range(steps+1):
            for first in range(26):
                for second in range(26):
                    # 65 - A
                    if step == 0:
                        rr = np.zeros(26, dtype=np.uint64)
                        rr[first] += 1
                        rr[second] += 1
                        memo_cache[first, second, step] = rr
                    else:
                        first_c = from_range_n_get_char(n=first)
                        second_c = from_range_n_get_char(n=second)
                        if f"{first_c}{second_c}" not in map_dic:
                            continue
                        to_insert = map_dic[f"{first_c}{second_c}"]
                        idx = map_char_to_range(c=to_insert)
                        rr = np.zeros(26, dtype=np.uint64)
                        rr[idx] = 1
                        memo_cache[first, second, step] = (memo_cache[first, idx, step-1] +
                                                           memo_cache[idx, second, step-1] -
                                                           rr)

        res = np.zeros(26, dtype=np.uint64)
        for i in range(1, len(template_s)):
            first = map_char_to_range(c=template_s[i-1])
            second = map_char_to_range(c=template_s[i])
            res = res + memo_cache[first, second, steps]
            if i < len(template_s) - 1:
                res[second] -= 1

        res_diff = max(res) - min((f for f in res if f > 0))
        print(res_diff)

def solve_1(steps: int = 1):
    with open(input_file, 'r', encoding='utf8') as f:
        template_s = list(f.readline().strip())
        map_dic = {line.strip().split(' -> ')[0]:line.strip().split(' -> ')[1]
               for line in f if line.strip() != ''}
        # steps: int = 10

        for _ in range(steps):
            arr = []
            for idx, s in enumerate(template_s):
                if idx == 0:
                    continue

                to_insert = map_dic[f"{template_s[idx-1]}{template_s[idx]}"]
                arr.append(template_s[idx-1])
                arr.append(to_insert)
            arr.append(template_s[-1])
            template_s = arr

    freq = [0 for _ in range(26)]
    for s in template_s:
        freq[ord(s) - ord('A')] += 1

    res = max(freq) - min((f for f in freq if f > 0))
    print(res)


if __name__ == '__main__':
    solve_1(steps=10)
    solve_2(steps=40)
    # lp = LineProfiler()
    # lp_wrapper = lp(solve_2)
    # lp_wrapper()
    # lp.print_stats()
