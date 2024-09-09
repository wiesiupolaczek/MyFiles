import random
import sys

J_NUMBERS = ["ichi", "ni", "san", "shi", "go", "roku"]  # Assuming these represent the dice faces

purse = 5000

while True:
    print(f"Masz {purse} monet. Ile chcesz postawić, lub Q aby zakończyć grę?")

    while True:
        pot = input("> ")
        if pot.upper() == "Q":
            print("Dzięki za grę!")
            sys.exit()
        elif not pot.isdecimal():
            print("Podaj kwotę w formie liczby.")
        elif int(pot) > purse:
            print("Nie masz tyle pieniędzy.")
        else:
            pot = int(pot)
            break

    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)

    print("Krupier potrząsa kubkiem.\nKrupier stawia kubek do góry dnem na podłodze\ni pyta, co obstawiasz.")
    print("     Nieparzyste (1) lub parzyste (2)?")

    while True:
        bet = input("> ")
        if bet != "2" and bet != "1":
            print("Proszę podać 1 lub 2.")
            continue
        else:
            break

    print("Krupier podnosi kubek: ")
    print(f" {J_NUMBERS[dice1-1]} - {J_NUMBERS[dice2-1]}")
    print(f" {dice1} - {dice2}")

    even = (dice2 + dice1) % 2 == 0
    correct = "2" if even else "1"

    win = bet == correct

    if win:
        print(f"Wygrales! Zabierasz {pot} monet.")
        purse += pot
    else:
        purse -= pot
        print("Przegrales.")

    if purse == 0:
        print("Nie masz już pieniędzy. Gra skończona.")
        sys.exit()
