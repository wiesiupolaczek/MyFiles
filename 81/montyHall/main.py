import random, sys


ALL_CLOESD = """
-----       -----       -----
|   |       |   |       |   |
| 1 |       | 2 |       | 3 |
|   |       |   |       |   |
-----       -----       -----
"""

FIRST_GOAT = """
-----       -----       -----
|   |       |   |       |   |
| K |       | 2 |       | 3 |
|   |       |   |       |   |
-----       -----       -----
"""

SECOND_GOAT = """
-----       -----       -----
|   |       |   |       |   |
| 1 |       | K |       | 3 |
|   |       |   |       |   |
-----       -----       -----
"""

THIRD_GOAT = """
-----       -----       -----
|   |       |   |       |   |
| 1 |       | 2 |       | K |
|   |       |   |       |   |
-----       -----       -----
"""

FIRST_CAR = """
-----       -----       -----
|   |       |   |       |   |
| A |       | K |       | K |
|   |       |   |       |   |
-----       -----       -----
"""

SECOND_CAR = """
-----       -----       -----
|   |       |   |       |   |
| K |       | A |       | K |
|   |       |   |       |   |
-----       -----       -----
"""
THIRD_CAR = """
-----       -----       -----
|   |       |   |       |   |
| K |       | K |       | A |
|   |       |   |       |   |
-----       -----       -----
"""

swapWins = 0
swapLosses = 0
stayWins = 0
stayLosses = 0


while True:
    carDoor = random.randint(1,3)
    while True:

        response = input("1-3 albo Q\n> ")
        if response.upper() == "Q":
            print("Dzieki za gre")
            sys.exit()

        if response in "123":
            break
    doorPick = int(response)

    while True:
        for i in range(1,4):
            if i != doorPick and i != carDoor:
                showGoatDoor = i
                break
        break

    if showGoatDoor == 1:
        print(FIRST_GOAT)
    elif showGoatDoor == 2:
        print(SECOND_GOAT)
    else:
        print(THIRD_GOAT)

    print(f"W bramce nr {showGoatDoor} jest koza")

    while True:
        print("Chcesz zmienic bramki T/N")
        swap = input("> ").upper()
        if swap == "T" or swap == "N":
            break

    if swap == "T":
        if (doorPick != 1 and showGoatDoor != 2) or (doorPick != 2 and showGoatDoor != 1):
            if showGoatDoor > doorPick:
                doorPick = showGoatDoor - doorPick
            else:
                doorPick = doorPick - showGoatDoor
        else:
            doorPick = 3

    if carDoor == 1:
        print(FIRST_CAR)
    elif carDoor == 2:
        print(SECOND_CAR)
    elif carDoor == 3:
        print(THIRD_CAR)

    print(f"W bramce nr {carDoor} jest samochod")

    if doorPick == carDoor:
        print("Wygrales")
        if swap == "T":
            swapWins += 1
        elif swap == "N":
            stayWins += 1
    else:
        print("Przegrales")
        if swap == "T":
            swapLosses += 1
        elif swap == "N":
            stayLosses += 1


    print("Koniec")