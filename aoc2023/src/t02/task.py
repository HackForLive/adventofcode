import os
import pathlib

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')

def check(name: str, val: int):
    dic_vals = {
        'red': 12,
        'green': 13,
        'blue': 14
    }

    if dic_vals[name] < val:
        return False
    return True


# @timer_decorator
def solve_1():
    with open(input_file, 'r', encoding='utf8') as f:
        res_sum = 0
        for line in f.readlines():
            l = line.strip()
            parts = l.split(':')
            game_id = parts[0].strip().split(' ')[1]
            print(game_id)
            bags = parts[1].strip().split(';')

            is_ok = True
            for part in bags:
                p = part.strip().split(',')
                # print(p)
                for i_b in p:
                    item = i_b.strip().split(' ')
                    print(f"{item[0] =}, {item[1] =}")
                    if not check(name=item[1], val=int(item[0])):
                        is_ok = False
                        break
                if not is_ok:
                    break
            if is_ok:
                res_sum += int(game_id)
        print(res_sum)

if __name__ == '__main__':
    solve_1()
