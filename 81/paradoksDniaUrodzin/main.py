import datetime, random


def getUrodziny(iloscDni):
    urodziny = []
    for i in range(iloscDni):
        startOfYear = datetime.date(2001, 1, 1)
        losowaLiczbaDni = datetime.timedelta(random.randint(0, 364))

        dUrodzin = startOfYear + losowaLiczbaDni
        urodziny.append(dUrodzin)
    return urodziny


def getMatch(urodziny):
    if len(urodziny) == len(set(urodziny)):
        return None
    for a, urodzinyA in enumerate(urodziny):
        for b, urodzinyB in enumerate(urodziny[a + 1:]):
            if urodzinyA == urodzinyB:
                return urodzinyA


MONTHS = ("Sty", "Lut", "Mar", "Kwi", "Maj", "Cze", "Lip", "Sie", "Wrz", "Paz", "Lis", "Gru")

while True:
    print("Ile urodzin powinienem wygenerowac")
    response = input("> ")
    if response.isdecimal() and (0 < int(response) <= 100):
        iloscDni = int(response)
        break
print()

print(f"Oto {iloscDni} dni urodzin:")
urodziny = getUrodziny(iloscDni)

for i, birthday in enumerate(urodziny):
    if i != 0:
        print(", ", end="")
    nMiesiaca = MONTHS[birthday.month -1]
    dateText = f"{nMiesiaca} {birthday.day}"
    print(dateText, end="")

print()
print()
match = getMatch(urodziny)
print("W tej symulacji, ", end = "")
if match != None:
    nMiesiaca = MONTHS[match.month - 1]
    dateText = f"{nMiesiaca} {match.day}"
    print("Kilka osob ma urodizny", dateText)
else:
    print("nie ma takich samych dni urodzin.")
print()

print(f"\n{getUrodziny(10)}")