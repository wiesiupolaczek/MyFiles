# odejmowanie=[]
# dodawanie=[]
# mnozenie=[]
# dzielenie=[]
#
# wejscie="10/2*8-2*5/10+2*3"
#
# def dzielonko(a,b):
#     return a/b
# w=[]
# w.append(wejscie)
#
# for i in w:
#         dodawanie.append(i.split("+"))
# for i in dodawanie:
#     for j in i:
#         odejmowanie.append(j.split("-"))
# for i in odejmowanie:
#     for j in i:
#         mnozenie.append(j.split("*"))
# for i in mnozenie:
#     for j in i:
#         dzielenie.append(j.split("/"))
#
# print(f"{dodawanie}\n{odejmowanie}\n{mnozenie}\n{dzielenie}\n")
#
# for i in range(len(dzielenie)):
#     if len(dzielenie[i])==2:
#         print(dzielonko(int(dzielenie[i][0]),int(dzielenie[i][1])))

def dzielenie(a,b):
    return a/b
def mnozenie(a,b):
    return a*b
def dodawanie(a,b):
    return a+b
def odejmowanie(a,b):
    return a-b
def szukajdzielenia():
    global znaki
    global dzialanie
    global erro
    dziel=dzialanie.find("/")
    if dziel > -1:
        ma=0
        mb=len(dzialanie)
        for z in znaki:
            miejscea=dzialanie[:dziel].rfind(z)
            if miejscea > ma:
                ma=miejscea
        for z in znaki:
            miejsceb=dzialanie[dziel+1:].find(z)

            if miejsceb < mb and miejsceb>=0:
                mb=miejsceb
        mb=mb+dziel+1

        ma1=ma
        ma2=dziel
        mb1=dziel
        mb2=mb
        if ma1==0:
            ma1=ma1-1


        try:
            a = float(dzialanie[ma1 + 1:ma2])
            b = float(dzialanie[mb1 + 1:mb2])
            wynik=dzielenie(a,b)
            dzialanie = dzialanie[:ma1 + 1] + str(wynik) + dzialanie[mb2:]
        except ValueError:
            print("Podawaj liczby")
            return 1
        except ZeroDivisionError:
            print("Nie mozna dzielic przez 0")
            erro = 1
            return 1


    else:
        return 1
def szukajmnozenia():

    global dzialanie
    global erro
    dziel=dzialanie.find("*")
    if dziel > -1:
        ma=0
        mb=len(dzialanie)
        for z in znaki:
            miejscea=dzialanie[:dziel].rfind(z)
            if miejscea > ma:
                ma=miejscea
        for z in znaki:
            miejsceb=dzialanie[dziel+1:].find(z)

            if miejsceb < mb and miejsceb>=0:
                mb=miejsceb
        mb=mb+dziel+1

        ma1=ma
        ma2=dziel
        mb1=dziel
        mb2=mb
        if ma1==0:
            ma1=ma1-1

        try:
            a = float(dzialanie[ma1 + 1:ma2])
            b = float(dzialanie[mb1 + 1:mb2])
            wynik=mnozenie(a,b)
            dzialanie = dzialanie[:ma1 + 1] + str(wynik) + dzialanie[mb2:]
        except ValueError:
            print("Podawaj liczby")
            erro=1
            return 1



    else:
        return 1

def szukajdodawania():

    global dzialanie
    global erro
    dziel=dzialanie.find("+")
    if dziel > -1:
        ma=0
        mb=len(dzialanie)
        for z in znaki:
            miejscea=dzialanie[:dziel].rfind(z)
            if miejscea > ma:
                ma=miejscea
        for z in znaki:
            miejsceb=dzialanie[dziel+1:].find(z)

            if miejsceb < mb and miejsceb>=0:
                mb=miejsceb
        mb=mb+dziel+1

        ma1=ma
        ma2=dziel
        mb1=dziel
        mb2=mb

        if ma1 ==0:
            ma1=ma1-1

        try:
            a = float(dzialanie[ma1 + 1:ma2])
            b = float(dzialanie[mb1 + 1:mb2])
            wynik = dodawanie(a, b)
            dzialanie = dzialanie[:ma1 + 1] + str(wynik) + dzialanie[mb2:]
        except ValueError:
            print("Podawaj liczby")
            erro=1
            return 1

    else:
        return 1
def szukajodejmowania():

    global dzialanie
    global erro
    dziel=dzialanie.find("-")
    if dziel > -1:
        ma=0
        mb=len(dzialanie)
        for z in znaki:
            miejscea=dzialanie[:dziel].rfind(z)
            if miejscea > ma:
                ma=miejscea
        for z in znaki:
            miejsceb=dzialanie[dziel+1:].find(z)

            if miejsceb < mb and miejsceb>=0:
                mb=miejsceb
        mb=mb+dziel+1

        ma1=ma
        ma2=dziel
        mb1=dziel
        mb2=mb
        if ma1 == 0:
            ma1=ma1-1

        try:
            a = float(dzialanie[ma1 + 1:ma2])
            b = float(dzialanie[mb1 + 1:mb2])
            wynik=odejmowanie(a,b)
            dzialanie = dzialanie[:ma1 + 1] + str(wynik) + dzialanie[mb2:]
        except ValueError:
            print("Podawaj liczby")
            erro=1
            return 1



    else:
        return 1

erro=0
wejscie=input("Dzialanie: ")
dzialanie=wejscie
stop=0
znaki=["/","*","-","+"]
while stop==0 and erro==0:

    if szukajdzielenia() == 1:
        if erro == 1:
            break
        if szukajmnozenia() == 1:
            if erro == 1:
                break
            if szukajodejmowania() == 1:
                if erro == 1:
                    break
                if szukajdodawania() == 1:
                    if erro == 1:
                        break
                    stop = 1
try:
    if float(dzialanie):
        print(dzialanie)
except ValueError:
    pass

