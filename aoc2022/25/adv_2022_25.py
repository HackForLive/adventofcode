import os

def convertSnafuToDec(snafu: str):
    res: int = 0
    n: int = len(snafu)
    for i in reversed(range(n)):
        sDigit = snafu[i]
        if sDigit.isnumeric():
            res += int(sDigit) * pow(5, n - (i + 1))
        elif sDigit == '-':
            res -= pow(5, n - (i + 1))
        elif sDigit == '=':
            res -= 2*pow(5, n - (i + 1))
        else:
            raise NotImplemented("No such digit: %s is supported" % (sDigit))
    return res

def convertDecToSnafu(dec: int):
    res: str = ""
    denom: int = 5

    r: int = 0
    curr: int = dec
    while curr > 0:
        mod: int = int(curr % denom)
        modr: int = int((curr + r) % denom)
        curr = int(curr / denom)

        if modr <= 2:
            if mod > 2: 
                r = 1
            else:
                r = 0
            res += str(modr)
        else:
            r = 1
            if denom - modr == 2:
                res += '='
            if denom - modr == 1:
                res += '-'
    if r > 0:
        res += str(r)
    return res[::-1]

if __name__ == "__main__" :
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt'), 'r')
    lines = f.readlines()

    l = []
    n = len(lines)             
    for i in range(n):
        snafu = lines[i].strip()
        l.append(convertSnafuToDec(snafu))

    res: int = sum(l)
    print(convertDecToSnafu(res))
