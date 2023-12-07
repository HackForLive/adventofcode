import os
import pathlib
import functools
from typing import Tuple

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


def parse():
    with open(input_file, 'r', encoding='utf8') as f:

        cards_bid = []
        for line in f:
            clean_l = line.strip()
            parts = clean_l.split(' ')

            cards = parts[0]
            bid = int(parts[1])
            cards_bid.append((cards, bid))
    return cards_bid

def get_card_rank_without_j(card: str):
    assert len(card) == 1
    ranks = {
        'A': 12,
        'K': 11, 
        'Q': 10,
        'J': 9,
        'T': 8,
        '9': 7,
        '8': 6,
        '7': 5,
        '6': 4,
        '5': 3, 
        '4': 2, 
        '3': 1,
        '2': 0
    }
    return ranks[card]

def get_card_rank_with_j(card: str):
    assert len(card) == 1
    ranks = {
        'A': 12,
        'K': 11, 
        'Q': 10,
        'T': 8,
        '9': 7,
        '8': 6,
        '7': 5,
        '6': 4,
        '5': 3, 
        '4': 2, 
        '3': 1,
        '2': 0,
        'J': -1
    }
    return ranks[card]


def get_type_rank_with_j(cards: str):
    cards_s = dict.fromkeys(cards, 0)
    for card in cards:
        cards_s[card] += 1

    if 'J' in cards_s:
        vals = sorted([value for key, value in cards_s.items() if key != 'J'])
        if cards_s['J'] == 5 or cards_s['J'] == 4:
            return 6
        if cards_s['J'] == 3:
            if vals == [2]:
                return 6
            elif vals == [1,1]:
                return 5
        if cards_s['J'] == 2:
            if vals == [3]:
                return 6
            elif vals == [1,2]:
                return 5
            elif vals == [1,1,1]:
                return 3
        if cards_s['J'] == 1:
            if vals == [4]:
                return 6
            elif vals == [1,3]:
                return 5
            elif vals == [2,2]:
                return 4
            elif vals == [1,1,2]:
                return 3
            elif vals == [1,1,1,1]:
                return 1
    # print(cards_s)
    vals = sorted(cards_s.values())
    # five same
    if vals == [5]:
        return 6
    # four same
    if vals == [1,4]:
        return 5
    # full house
    if vals == [2,3]:
        return 4
    # three same
    if vals == [1,1,3]:
        return 3
    # two pair
    if vals == [1,2,2]:
        return 2
    if vals == [1,1,1,2]:
        return 1
    return 0


def get_type_rank(cards: str):
    cards_s = dict.fromkeys(cards, 0)
    for card in cards:
        cards_s[card] += 1

    vals = sorted(cards_s.values())
    # five same
    if vals == [5]:
        return 6
    # four same
    if vals == [1,4]:
        return 5
    # full house
    if vals == [2,3]:
        return 4
    # three same
    if vals == [1,1,3]:
        return 3
    # two pair
    if vals == [1,2,2]:
        return 2
    if vals == [1,1,1,2]:
        return 1
    return 0

def compare(item1: Tuple[str, int], item2: Tuple[str, int]):
    rank1 = get_type_rank(item1[0])
    rank2 = get_type_rank(item2[0])
    # continue
    if rank1 == rank2:
        for i in range(len(item1[0])):
            rank1 = get_card_rank_without_j(card=item1[0][i])
            rank2 = get_card_rank_without_j(card=item2[0][i])
            if rank1 != rank2:
                break
    if rank1 > rank2:
        return -1
    if rank2 > rank1:
        return 1
    return 0

def compare_with_j(item1: Tuple[str, int], item2: Tuple[str, int]):
    rank1 = get_type_rank_with_j(item1[0])
    rank2 = get_type_rank_with_j(item2[0])
    # continue
    if rank1 == rank2:
        for i in range(len(item1[0])):
            rank1 = get_card_rank_with_j(card=item1[0][i])
            rank2 = get_card_rank_with_j(card=item2[0][i])
            if rank1 != rank2:
                break
    if rank1 > rank2:
        return -1
    if rank2 > rank1:
        return 1
    return 0

def solve_1():
    cards_bid = parse()

    cards_bid_sorted = sorted(cards_bid, key=functools.cmp_to_key(compare))
    # print(cards_bid_sorted)
    sum_r = 0
    for j, card in enumerate(reversed(cards_bid_sorted)):
        sum_r += (j+1)*card[1]
    print(sum_r)


def solve_2():
    cards_bid = parse()

    cards_bid_sorted = sorted(cards_bid, key=functools.cmp_to_key(compare_with_j))
    # print(cards_bid_sorted)
    sum_r = 0
    for j, card in enumerate(reversed(cards_bid_sorted)):
        sum_r += (j+1)*card[1]
    print(sum_r)

if __name__ == '__main__':
    solve_1()
    solve_2()
