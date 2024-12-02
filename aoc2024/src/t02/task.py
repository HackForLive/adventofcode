from pathlib import Path

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'


@timer_decorator
def solve_1(p: Path):
    with open(p, 'r', encoding='utf8') as f:
        res = 0
        for line in f:
            nums = [int(i) for i in line.strip().split(' ')]

            is_in = True
            is_de = True
            for i in range(len(nums)-1):
                if 1 <= nums[i+1]-nums[i] <= 3:
                    is_de = False
                    is_in = True if is_in else False
                elif 1 <= nums[i]-nums[i+1] <= 3:
                    is_de = True if is_de else False
                    is_in = False
                else:
                    is_in = False
                    is_de = False
            
            if (is_in and not is_de) or (not is_in and is_de): 
                res += 1 


        return res


@timer_decorator
def solve_2(p: Path):
    with open(p, 'r', encoding='utf8') as f:
        res = 0
        for line in f:
            nums = [int(i) for i in line.strip().split(' ')]

            is_in = True
            comp = 0

            i = 0
            while i < len(nums)-1:
                if 1 <= nums[i+1]-nums[i] <= 3:
                    is_in = True if is_in else False
                else:
                    if comp == 0:
                        comp = 1
                        if i + 1 < len(nums) - 1:
                            is_ok = (1 <= nums[i+2]-nums[i+1] <= 3) 
                            if i > 0:
                                is_ok &= (1 <= nums[i+1]-nums[i-1] <= 3) 
                            
                            is_ok |= (1 <= nums[i+2]-nums[i] <= 3)
                            if not is_ok:
                                is_in = False
                                break
                            i += 1
                    else:
                        is_in = False
                        break
                i += 1

            is_de = True
            comp = 0

            i = 0
            while i < len(nums)-1:
                if 1 <= nums[i]-nums[i+1] <= 3:
                    is_de = True if is_de else False
                else:
                    if comp == 0:
                        comp = 1
                        if i + 1 < len(nums) - 1:


                            is_ok = (1 <= nums[i+1]-nums[i+2] <= 3)
                            if i > 0:
                                is_ok &= (1 <= nums[i-1]-nums[i+1] <= 3)

                            is_ok |= (1 <= nums[i]-nums[i+2] <= 3)
                           
                            if not is_ok:
                                is_de = False
                                break
                            i += 1
                    else:
                        is_de = False
                        break
                i += 1
                
            if (is_in and not is_de) or (not is_in and is_de): 
                res += 1
        return res


if __name__ == '__main__':
    test_o = solve_1(p=t_f)

    print(test_o)
    if test_o != 2:
        raise ValueError('Test failed!')
    
    f_o = solve_1(p=in_f)
    if f_o != 585:
        raise ValueError('The first task failed!')
    
    test_o = solve_2(p=t_f)
    if test_o != 4:
        raise ValueError('Test failed!')
    
    s_o = solve_2(p=in_f)
    if s_o != 626:
        raise ValueError('The second task failed!')

    print("All passed!")
