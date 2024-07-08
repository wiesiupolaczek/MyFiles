wynik=0
def dodawanie(dzial):
    global wynik
    dzialcopy = dzial
    dzial = dzial.split("+")
    if len(dzial) != 1:
        try:
            for i in range(len(dzial)):
                wynik=wynik+int(dzial[i])
            print(f"{dzialcopy}={wynik}")
        except (ValueError, UnboundLocalError):
            print("Podawaj liczby")

def odejmowanie(dzial):
    global wynik
    dzialcopy = dzial
    dzial = dzial.split("-")
    if len(dzial) != 1:
        try:
            wynik=wynik + int(dzial[0])
            for i in range(1,len(dzial)):
                wynik = wynik - int(dzial[i])
            print(f"{dzialcopy}={wynik}")
        except (ValueError, UnboundLocalError):
            print("Podawaj liczby")

def mnozenie(dzial):
    global wynik
    dzialcopy = dzial
    dzial = dzial.split("*")
    if len(dzial) != 1:
        try:
            wynik = wynik + int(dzial[0])
            for i in range(1, len(dzial)):
                wynik = wynik * int(dzial[i])
            print(f"{dzialcopy}={wynik}")
        except (ValueError, UnboundLocalError):
            print("Podawaj liczby")

def dzielenie(dzial):
    global wynik
    dzialcopy = dzial
    dzial = dzial.split("/")
    if len(dzial) != 1:
        try:
            wynik = wynik + int(dzial[0])
            for i in range(1, len(dzial)):
                wynik = wynik / int(dzial[i])
            print(f"{dzialcopy}={wynik}")
        except (ZeroDivisionError, UnboundLocalError):
            print("Nie mozna dzielic przez 0")
        except (ValueError, UnboundLocalError):
            print("Podawaj liczby")







if __name__ == '__main__':
    q=1
    while q==1:
        print("Instrukcje:\nQ,q-wyjscie\n' + ' - dodawanie\n' - ' - odejmowanie\n' / ' - dzielenie\n' * ' - mnozenie\ne.g.10*10*9*8...\n---------------------------------")
        wynik=0
        dzial=input("Dzialanie:\n")
        if dzial == "q" or dzial == "Q":
            q=0
            break;
        else:

            dzielenie(dzial)
            mnozenie(dzial)
            odejmowanie(dzial)
            dodawanie(dzial)
