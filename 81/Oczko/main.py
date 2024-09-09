import random,sys
def getBet(maxBet):
    while True:
        print()
        bet = input(f"Ile chcesz postawic? 1 - {maxBet} lub Q\n> ".upper().strip())
        if bet == "Q":
            print("Dzieki za gre")
            sys.exit()

        if not bet.isdecimal():
            continue

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet

def getDeck():
    deck = []
    for suit in (HEARTS, DIMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ("J","Q","K","A"):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

def displayHands(pHand,dHand,showDealerHand):
    print()
    if showDealerHand:
        print("Krupier:",getHandValue(dHand))
        displayCards(dHand)
    else:
        print("Krupier: ???:")
        displayCards([BACKSIDE] +dHand[1:])

    print("Gracz:",getHandValue(pHand))
    displayCards(pHand)

def displayCards(cards):
    row = ["","","","",""]
    for i, card in enumerate(cards):
        row[0] += "___"
        if card == BACKSIDE:
            row[1] += "|## |"
            row[2] += "|###|"
            row[3] += "|_##|"
        else:
            rank, suit = card
            row[1] += f"|{rank.ljust(2)} |"
            row[2] += f"| {suit} |"
            row[3] += f"|_{rank.rjust(2, "_")}|"

    for ro in row:
        print(ro)

def getMove(pHand, money):
    while True:
        moves = ["(D)obierz","(S)top"]

        if len(pHand) == 2 and money > 0:
            moves.append("(P)odwoj")

        movePrompt = ", ".join(moves) + "> "
        move = input(movePrompt).upper()
        if move in ("D","S"):
            return move
        if move == "P" and "(P)odwoj" in moves:
            return move

def getHandValue(cards):
    value = 0
    numberOfAces = 0

    for card in cards:
        rank = card[0]
        if rank == "A":
            numberOfAces += 1
        elif rank in ("J","Q","K"):
            value += 10
        else:
            value += int(rank)

    value += numberOfAces
    for i in range(numberOfAces):
        if value + 10 <= 21:
            value += 10
    return value

HEARTS = chr(9829)
DIMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)

BACKSIDE = "tyl"

money = 5000
while True:
    if money <= 0:
        print("Dzieki za gre")
        break

    print(f"Budzet: {money}")
    bet = getBet(money)


    deck = getDeck()
    pHand = [deck.pop(),deck.pop()]
    dHand = [deck.pop(),deck.pop()]


    print(f"Zalad: {bet}")
    while True:
        displayHands(pHand,dHand,False)
        print()

        if getHandValue(pHand) > 21:
            break

        move = getMove(pHand, money - bet)

        if move == "P":

            additionalBet = getBet(min(bet, (money - bet)))
            bet += additionalBet
            print(f"Zaklad zwiekszony do kwoty {bet}")

        if move in ("D","P"):
            newCard = deck.pop()
            rank, suit = newCard
            print(f"Wziales {rank} {suit}")
            pHand.append(newCard)

            if getHandValue(pHand) > 21:
                continue

        if move in ("S", "P"):
            break

        if getHandValue(pHand) <= 21:
            while getHandValue(dHand) < 17:
                print("Krupier dobiera karte...")
                dHand.append(deck.pop())
                displayHands(pHand,dHand, False)

                if getHandValue(dHand) > 21:
                    break

                input("Kontynnuj\n\n")

        displayHands(pHand, dHand, True)

        pValue = getHandValue(pHand)
        dValue = getHandValue(dHand)

        if dValue > 21:
            print(f"Krupier przegral wygrales {bet}")
            money += bet

        elif dValue > pValue or pValue > 21:
            print(f"Przegrales {bet}")
            money -= bet

        elif pValue > dValue:
            print(f"Wygrales {bet}")
            money += bet

        elif pValue == dValue:
            print("Remis")

        input("Kontynnuj: \n\n")
