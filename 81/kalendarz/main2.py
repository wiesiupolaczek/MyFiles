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


    currnetDate = datetime.date(year,month,1)
    while currnetDate.weekday() != 6:
        currnetDate -= datetime.timedelta(days=1)

    while True:


        dayNumRow = ""
        for i in range(7):

            dayNumLabel = str(currnetDate.day).rjust(2) +"."+ str(miesiace[currnetDate.month - 1][:3]+"  ")
            dayNumRow +=dayNumLabel
            currnetDate += datetime.timedelta(days=1)
        dayNumRow += "\n"

        callText += dayNumRow


        if currnetDate.month != month:
            break


    return callText
callText = getCalendar(rok,miesiac)
print(callText)
