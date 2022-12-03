import os

max = 0
loopMax = 0
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input1.txt')) as fp:
    for line in fp:
        loopMax = 0 if line.strip() == "" else int(line) + loopMax
        max = loopMax if loopMax > max else max
print(max)
