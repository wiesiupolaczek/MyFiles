import random

HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)

def getDeck():
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ("J", "Q", "K", "A"):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


while True:
    deck = getDeck()
    table = [deck.pop(), deck.pop(), deck.pop()]

    pHand = [deck.pop(),deck.pop()]
    h1 = []
    h2 = []
    h3 = []
    h4 = []
    for i in range(2):
        pHand.append(deck.pop())
        h1.append(deck.pop())
        h2.append(deck.pop())
        h3.append(deck.pop())
        h4.append(deck.pop())
    break

print(deck)



