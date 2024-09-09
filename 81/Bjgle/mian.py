import random

znaki = 3
proby = 10

def snumber():
    numbers = list("0123456789")
    random.shuffle(numbers)
    snum = ""
    for i in range(znaki):
        snum += str(numbers[i])
    return snum
def clues(guess,secretnumber):
    if guess == secretnumber:
        return "Udalo sie"

    clue=[]
    for i in range(len(guess)):
        if guess[i] == secretnumber[i]:
            clue.append("Fermi")
        elif guess[i] in secretnumber:
            clue.append("Piko")

    if len(clue) == 0:
        return "Bajgle"
    else:
        clue.sort()
        return " ".join(clue)
def main():
    while True:
        snum=snumber()
        print("Mam na mysli liczbe")
        print(f"Masz {proby} prob aby odgadna jaka to liczba.")

        numGuesses = 1
        while numGuesses <= proby:
            guess = ""
            while len(guess) != znaki or not guess.isdecimal():
                print(f"Proba #{numGuesses}")
                guess = input("Podaj liczbe")
            clue = clues(guess,snum)
            print(clue)
            numGuesses += 1

            if guess == snum:
                break
            if numGuesses >= proby:
                print("Wykorzystales wszystkie proby")
                print(f"Prawidlowa odpowiedz to {snum}")
        print("Czy chcesz zagrac jeszcze raz? (t/n)")
        if not input("> ").lower().startswith("t"):
            break
    print("Dziekuje za gre")


if __name__ == "__main__":
    main()