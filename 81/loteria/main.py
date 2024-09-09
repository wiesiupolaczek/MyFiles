import random

while True:
    numbers = input("Podaj 5 roznych liczb od 1 do 69 odzielonych spacja\n")

    liczby = numbers.split()
    if len(liczby) != 5:
        print("Podaj 5 liczb oddzielonych spacja")
        continue
    try:
        for i in range(5):
            liczby[i] = int(liczby[i])
    except ValueError:
        print("Podaj liczby")
        continue

    for i in liczby:
        if not (1 <= i <=69):
            print("Liczby musza byc od 1 do 69")
            continue
    if len(set(liczby)) != 5:
        print("Musisz podac 5 roznych liczb")
        continue
    break

while True:
    numbers = input("Podaj liczbe od 1 do 26\n")

    power = numbers.split()
    try:
        for i in range(1):
            power = int(power[i])
    except ValueError:
        print("Podaj liczby")
        continue
    if not (1 <= power <=26):
        print("Liczby musza byc od 1 do 26")
        continue
    break


while True:
    proby = input("Podaj liczbe prob\n")

    try:
        proby = int(proby)
    except ValueError:
        print("Podaj liczbe")
        continue

    break

print(f"Musisz wydac {proby * 2}\n")

posibleNumbers = list(range(1,70))
for i in range(proby):
    random.shuffle(posibleNumbers)
    winnNumbers = posibleNumbers[:5]
    winnPowerball = random.randint(1,26)

    print("Szczesliwe liczby to: ", end="")
    allNumbers = ""
    for i in range(5):
        allNumbers += str(winnNumbers[i]) + " "
    allNumbers += "oraz " + str(winnPowerball)
    print(allNumbers.ljust(21),end="")

    if (set(winnNumbers) == set(liczby)) and winnPowerball == power:
        print(f"Wygrales\nTwoje liczby to {set(liczby)} a wygrywajace to {set(winnNumbers)}")
        break
    else:
        print(f"Przegrales")
