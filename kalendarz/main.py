import datetime

dni = ("Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela")
miesiace = ("Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień")


while True:
    rok = input("Podaj rok ")

    if rok.isdecimal() and int(rok) > 0:
        rok = int(rok)
        break

    print("Podaj wartosc liczbowa np. 2023")
    continue

while True:
    miesiac = input("Podaj miesiac ")
    if not miesiac.isdecimal():
        print("Podaj liczbe")
    miesiac = int(miesiac)
    if 1 <= miesiac <= 12:
        break
    print("Podaj liczbe od 1 do 12")

def getCalendar(year,month):
    callText= ""

    weeksep = ("+---------" * 7) + "\n"
    blankro = ("|         " * 7) + "|\n"
    currnetDate = datetime.date(year,month,1)
    while currnetDate.weekday() != 6:
        currnetDate -= datetime.timedelta(days=1)

    while True:
        callText += weeksep

        dayNumRow = ""
        for i in range(7):
            dayNumLabel = str(currnetDate.day).rjust(2)
            dayNumRow += "|" + dayNumLabel + "       "
            currnetDate += datetime.timedelta(days=1)
        dayNumRow += "|\n"

        callText += dayNumRow
        for i in range(3):
            callText += blankro

        if currnetDate.month != month:
            break

    callText += weeksep
    return callText
callText = getCalendar(rok,miesiac)
print(callText)
