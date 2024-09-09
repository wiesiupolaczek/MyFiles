import requests


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

print(imieniny(20, 10))



"""
def getCalendar(year, month):
    callText = ""
    weeksep = ("+---------" * 7) + "+\n"
    blankro = ("|         " * 7) + "|\n"
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
            dayNumRow += "|" + dayNumLabel + "       "

            if currnetDate.month == month:
                namedays = imieniny(currnetDate.day, currnetDate.month)
                if len(namedays) >= 1:
                    nameday1Label = namedays[0][:7].ljust(8)
                else:
                    nameday1Label = "       "
                if len(namedays) >= 2:
                    nameday2Label = namedays[1][:7].ljust(8)
                else:
                    nameday2Label = "        "
            else:
                nameday1Label = "        "
                nameday2Label = "        "

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

"""
