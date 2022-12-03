import os
# A for Rock, B for Paper, and C for Scissors
# response: X for Rock, Y for Paper, and Z for Scissors

# Your total score is the sum of your scores for each round.
# The score for a single round is the score for the shape you selected 
# (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score 
# for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

# Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock

scores = {
    'A X': 3,
    'A Y': 6,
    'A Z': 0,
    'B X': 0,
    'B Y': 3,
    'B Z': 6,
    'C X': 6,
    'C Y': 0,
    'C Z': 3
}

values = {
    'X': 1,
    'Y': 2,
    'Z': 3
}
sum = 0
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input2.txt')) as fp:
    for line in fp:
        a = line.split(' ')[0].strip()
        b = line.split(' ')[1].strip()
        sum = sum + values[b] + scores["%s %s" % (a,b)]
print(sum)
