from aocd import submit
from aocd.models import Puzzle
from enum import Enum

card_order = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
card_order_b = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

class Hands(Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIRS = 2
    ONE_PAIR = 1
    HIGH_CARD = 0



def type_of_hand(hand):
    labels = {}
    for card in hand:
        if card not in labels:
            labels[card] = 1
        else:
            labels[card] += 1
    if len(labels) == 5:
        return Hands.HIGH_CARD.value
    elif len(labels) == 1:
        return Hands.FIVE_OF_A_KIND.value
    elif len(labels) == 2:
        for card, count in labels.items():
            if count == 4 or count == 1:
                return Hands.FOUR_OF_A_KIND.value
            else:
                return Hands.FULL_HOUSE.value
    elif len(labels) == 3:
        for card, count in labels.items():
            if count == 3:
                return Hands.THREE_OF_A_KIND.value
        return Hands.TWO_PAIRS.value
    elif len(labels) == 4:
        return Hands.ONE_PAIR.value
    else:
        print("WTF")

def type_of_hand_b(hand):
    if "J" not in hand:
        return type_of_hand(hand)
    labels = {}
    for card in hand:
        if card not in labels:
            labels[card] = 1
        else:
            labels[card] += 1
    top_card = "J"
    top_count = 0
    for card, count in labels.items():
        if count > top_count and card != "J":
            top_card = card
            top_count = count
    hand = hand.replace("J", top_card)
    return type_of_hand(hand)

def compare_top_card(hand1, hand2, card_power=card_order):
    for c1, c2 in zip(hand1, hand2):
        if c1 == c2:
            continue
        i1 = card_power.index(c1)
        i2 = card_power.index(c2)
        return i1 < i2

def a(data):
    hands = []
    bets = []
    for line in data.split("\n"):
        hand, bet = line.split()
        hands.append(hand)
        bets.append(int(bet))
    hand_values = [type_of_hand(hand) for hand in hands]
    hand_types = sorted(list(set(hand_values)))
    points = len(hands)
    winnings = 0
    for value in reversed(hand_types):
        hands_and_bets = [(hands[i], bets[i]) for i, x in enumerate(hand_values) if x == value]
        while len(hands_and_bets) > 1:
            winner = hands_and_bets[0]
            for x in hands_and_bets:
                if not compare_top_card(winner[0], x[0]):
                    winner = x
            winnings += winner[1] * points
            points -= 1
            hands_and_bets.remove(winner)
        winnings += hands_and_bets[0][1] * points
        points -= 1
    return winnings

def b(data):
    hands = []
    bets = []
    for line in data.split("\n"):
        hand, bet = line.split()
        hands.append(hand)
        bets.append(int(bet))
    hand_values = [type_of_hand_b(hand) for hand in hands]
    hand_types = sorted(list(set(hand_values)))
    points = len(hands)
    winnings = 0
    for value in reversed(hand_types):
        hands_and_bets = [(hands[i], bets[i]) for i, x in enumerate(hand_values) if x == value]
        while len(hands_and_bets) > 1:
            winner = hands_and_bets[0]
            for x in hands_and_bets:
                if not compare_top_card(winner[0], x[0], card_power=card_order_b):
                    winner = x
            winnings += winner[1] * points
            points -= 1
            hands_and_bets.remove(winner)
        winnings += hands_and_bets[0][1] * points
        points -= 1
    return winnings


year = 2023
day = 7

p = Puzzle(year=year, day=day)
data = p.input_data

example_data_a = p.examples[0].input_data
example_answer_a = p.examples[0].answer_a

assert(a(example_data_a)==int(example_answer_a))
assert(a(data)==251216224)
#submit(a(data), part="a", year=year, day=day)


example_data_b = example_data_a
example_answer_b = 5905

assert(b(example_data_b)==example_answer_b)
assert(b(data)==250825971)
#submit(b(data), part="b", year=year, day=day)
