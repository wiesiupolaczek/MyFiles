import random, sys

J_NUMBERS = ["ichi", "ni", "san", "shi", "go", "roku"]


purse = 5000

while True:
    print(f"Masz {purse} monet ile chcesz postawic lub Q")

    while True:
        pot = input("> ")
        if pot.upper() == "Q":
            print("Dzieki za gre")
            sys.exit()

        elif not pot.isdecimal():
            print("Podaj kwote")
        elif int(pot) >purse:
            print("Nie masz tyle pieniedzy")
        else:
            pot = int(pot)
            break
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)

        print("Krupier potrzasa kobkiem \nKrupier stawia kupek do gory dnem na podlodze\ni pyta co obstawiasz\n")
        print("     Niepazyste  (1) lub parzyste (2)?")

        while True:
            bet = input("> ")
            if bet != "2" and bet != "1":
                print("Prosze podac 1 lub 2")
                continue
            else:
                break

        print("Krupier podnosi kubek: ")
        print(f" {J_NUMBERS[dice1-1]} - {J_NUMBERS[dice2-1]}")
        print(f" {dice1} - {dice2}")


        even = (dice2 + dice1) % 2 ==0
        if even:
            correct = "2"
        else:
            correct = "1"

        win = bet == correct

        if win:
            print(f"Wygrales Zabierasz {pot}")
            purse += pot

        else:
            purse -= pot
            print("Przegrales")

        if purse == 0:
            print("Nie masz juz pieniedzy")
            sys.exit()