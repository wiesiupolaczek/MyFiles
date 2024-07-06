
def dodawanie():
    a = input("Podaj liczbe a : ")
    b = input("Podaj liczbe b: ")
    wynik=int(a)+int(b)
    print(f"{a}+{b}={wynik}")
def odejmowanie():
    a = input("Podaj liczbe a : ")
    b = input("Podaj liczbe b: ")
    wynik=int(a)-int(b)
    print(f"{a}-{b}={wynik}")

def mnozenie():
    a = input("Podaj liczbe a : ")
    b = input("Podaj liczbe b: ")
    wynik=int(a)*int(b)
    print(f"{a}*{b}={wynik}")

def dzielenie():
    a = input("Podaj liczbe a : ")
    b = input("Podaj liczbe b: ")
    wynik=int(a)/int(b)
    print(f"{a}:{b}={wynik}")

if __name__ == '__main__':
    on=1
    while on==1:
        print("Kalkulator")
        o=int(input("Co chces zrobic?\n1)Dodawanie\n2)Odejmowanie\n3)Mnozenie\n4)Dzielenie\n "))
        if o==1:
            dodawanie()
        elif o==2:
            odejmowanie()
        elif o==3:
            mnozenie()
        elif o==4:
            dzielenie()
        else:
            on=0
