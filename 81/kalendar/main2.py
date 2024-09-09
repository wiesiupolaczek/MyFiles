import datetime
import requests
import random

dni = ("Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela")
miesiace = ("Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień")

def imieniny(day, month):
    url = 'https://nameday.abalin.net/api/V1/getdate'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    params = {
        'day': day,
        'month': month,
        'country': 'pl'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        value = data["nameday"]
        names = value["pl"].split(", ")
        if names[0].endswith(","):
            names[0] = names[0][:-1]
        return names
    return []

while True:
    rok = input("Podaj rok ")
    if rok.isdecimal() and int(rok) > 0:
        rok = int(rok)
        break
    print("Podaj wartosc liczbowa np. 2023")

while True:
    miesiac = input("Podaj miesiac ")
    if not miesiac.isdecimal():
        print("Podaj liczbe")
    miesiac = int(miesiac)
    if 1 <= miesiac <= 12:
        break
    print("Podaj liczbe od 1 do 12")

def getCalendar(year, month):
    callText = ""
    weeksep = ("+--------------" * 7) + "+\n"  # Increased width
    blankro = ("|              " * 7) + "|\n"  # Increased width
    currnetDate = datetime.date(year, month, 1)
    while currnetDate.weekday() != 6:
        currnetDate -= datetime.timedelta(days=1)

    while True:
        callText += weeksep
        dayNumRow = ""
        nameday1Row = ""
        nameday2Row = ""
        for i in range(7):
            dayNumLabel = str(currnetDate.day).rjust(2)
            dayNumRow += "|" + dayNumLabel + "            "

            if currnetDate.month == month:
                namedays = imieniny(currnetDate.day, currnetDate.month)
                if len(namedays) > 2:
                    selected_namedays = random.sample(namedays, 2)
                else:
                    selected_namedays = namedays

                nameday1Label = selected_namedays[0][:12].ljust(13) if len(selected_namedays) >= 1 else "             "
                nameday2Label = selected_namedays[1][:12].ljust(13) if len(selected_namedays) >= 2 else "             "
            else:
                nameday1Label = "             "
                nameday2Label = "             "

            nameday1Row += "|" + nameday1Label + " "
            nameday2Row += "|" + nameday2Label + " "

            currnetDate += datetime.timedelta(days=1)
        dayNumRow += "|\n"
        nameday1Row += "|\n"
        nameday2Row += "|\n"

        callText += dayNumRow + nameday1Row + nameday2Row

        if currnetDate.month != month:
            break

    callText += weeksep
    return callText
callText = getCalendar(rok, miesiac)
print(callText)