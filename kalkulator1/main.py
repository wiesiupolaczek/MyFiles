
def dodawanie():
    try:
        a = input("Podaj liczbe a : ")
        b = input("Podaj liczbe b: ")
        wynik=int(a)+int(b)
        print(f"{a}+{b}={wynik}")
    except ValueError:
        print("To nie liczba")

def odejmowanie():
    try:
        a = input("Podaj liczbe a : ")
        b = input("Podaj liczbe b: ")
        wynik=int(a)-int(b)
        print(f"{a}-{b}={wynik}")
    except ValueError:
        print("To nie liczba")

def mnozenie():
    try:
        a = input("Podaj liczbe a : ")
        b = input("Podaj liczbe b: ")
        wynik=int(a)*int(b)
        print(f"{a}*{b}={wynik}")
    except ValueError:
        print("To nie liczba")

def dzielenie():
    try:
        a = input("Podaj liczbe a : ")
        b = input("Podaj liczbe b: ")
        wynik=int(a)/int(b)
        print(f"{a}:{b}={wynik}")
    except ValueError:
        print("To nie liczba")


if __name__ == '__main__':
    on=1
    while on==1:
        print("Kalkulator")

        try:
            o = int(input("Co chces zrobic?\n1)Dodawanie\n2)Odejmowanie\n3)Mnozenie\n4)Dzielenie\n5)Wyjscie\n "))
            if o==1:
                dodawanie()
            elif o==2:
                odejmowanie()
            elif o==3:
                mnozenie()
            elif o==4:
                dzielenie()
            elif o==5:
                on=0
        except ValueError:
            print(" ^  To nie liczba\n")
