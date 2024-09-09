import random

# Define card values and suits
wartosci = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10,
            'A': 11}
kolory = {'Kier': '♥', 'Karo': '♦', 'Trefl': '♣', 'Pik': '♠'}


# Define a function to create a deck of cards
def utworz_talie():
    talia = []
    for kolor in kolory:
        for wartosc, punkty in wartosci.items():
            talia.append((wartosc, kolor, punkty))
    random.shuffle(talia)
    return talia


# Define a function to calculate the total points of a hand
def oblicz_punkty(reka):
    suma_punktow = sum(karta[2] for karta in reka)
    asy = sum(1 for karta in reka if karta[0] == 'A')
    while suma_punktow > 21 and asy:
        suma_punktow -= 10
        asy -= 1
    return suma_punktow


# Define a function to print cards
def drukuj_karty(reka, ukryta=False):
    lines = ["", "", "", "", ""]
    for j, karta in enumerate(reka):
        if ukryta and j == 1:
            lines[0] += "┌───────┐ "
            lines[1] += "│░░░░░░░│ "
            lines[2] += "│░░░░░░░│ "
            lines[3] += "│░░░░░░░│ "
            lines[4] += "└───────┘ "
        else:
            wartosc, kolor = karta[0], kolory[karta[1]]
            lines[0] += "┌───────┐ "
            lines[1] += f"│{wartosc:<2}     │ "
            lines[2] += f"│   {kolor}   │ "
            lines[3] += f"│     {wartosc:>2}│ "
            lines[4] += "└───────┘ "
    for line in lines:
        print(line)


# Define the main game function
def graj():
    talia = utworz_talie()
    reka_gracza = []
    reka_krupiera = []

    # Initial deal
    reka_gracza.append(talia.pop())
    reka_gracza.append(talia.pop())
    reka_krupiera.append(talia.pop())
    reka_krupiera.append(talia.pop())

    # Player's turn
    while True:
        print("\nTwoja ręka:")
        drukuj_karty(reka_gracza)
        print("Punkty gracza:", oblicz_punkty(reka_gracza))

        print("\nRęka krupiera:")
        drukuj_karty(reka_krupiera, ukryta=True)

        if oblicz_punkty(reka_gracza) == 21:
            print("Blackjack! Wygrywasz!")
            return

        ruch = input("Czy chcesz dobrać kartę? (tak/nie): ").lower()
        if ruch == 'tak':
            reka_gracza.append(talia.pop())
            if oblicz_punkty(reka_gracza) > 21:
                print("\nTwoja ręka:")
                drukuj_karty(reka_gracza)
                print("Punkty gracza:", oblicz_punkty(reka_gracza))
                print("Przekroczyłeś 21 punktów. Przegrywasz.")
                return
        else:
            break

    # Dealer's turn
    while oblicz_punkty(reka_krupiera) < 17:
        reka_krupiera.append(talia.pop())

    print("\nTwoja ręka:")
    drukuj_karty(reka_gracza)
    print("Punkty gracza:", oblicz_punkty(reka_gracza))

    print("\nRęka krupiera:")
    drukuj_karty(reka_krupiera)
    print("Punkty krupiera:", oblicz_punkty(reka_krupiera))

    if oblicz_punkty(reka_krupiera) > 21 or oblicz_punkty(reka_gracza) > oblicz_punkty(reka_krupiera):
        print("Wygrywasz!")
    elif oblicz_punkty(reka_gracza) < oblicz_punkty(reka_krupiera):
        print("Przegrywasz.")
    else:
        print("Remis.")


# Run the game
if __name__ == "__main__":
    graj()
