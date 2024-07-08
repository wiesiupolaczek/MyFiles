def dodawanie(dzial):
    dzial = dzial.split("+")
    if len(dzial) != 1:
        try:
            wynik=int(dzial[0])+int(dzial[1])
            print(f"{dzial[0]}+{dzial[1]}={wynik}")
        except (ValueError, UnboundLocalError):
            print("Podawaj liczby")

def odejmowanie(dzial):
    dzial = dzial.split("-")
    if len(dzial) != 1:
        try:
            wynik=int(dzial[0])-int(dzial[1])
            print(f"{dzial[0]}-{dzial[1]}={wynik}")
        except (ValueError, UnboundLocalError):
            print("Podawaj liczby")

def mnozenie(dzial):
    dzial = dzial.split("*")
    if len(dzial) != 1:
        try:
            wynik=int(dzial[0])*int(dzial[1])
            print(f"{dzial[0]}*{dzial[1]}={wynik}")
        except (ValueError, UnboundLocalError):
            print("Podawaj liczby")

def dzielenie(dzial):
    dzial = dzial.split("/")
    if len(dzial) != 1:
        try:
            wynik=int(dzial[0])/int(dzial[1])
            print(f"{dzial[0]}/{dzial[1]}={wynik}")
        except (ZeroDivisionError, UnboundLocalError):
            print("Nie mozna dzielic przez 0")
        except (ValueError, UnboundLocalError):
            print("Podawaj liczby")







if __name__ == '__main__':
    q=1
    print("Instrukcje:\nQ,q-wyjscie\n' + ' - dodawanie\n' - ' - odejmowanie\n' / ' - dzielenie\n' * ' - mnozenie\ne.g.10+11\n----------------------------------------")
    while q==1:
        dzial=input("Dzialanie:\n")
        if dzial == "q" or dzial == "Q":
            q=0
            break;
        else:

            dzielenie(dzial)
            mnozenie(dzial)
            odejmowanie(dzial)
            dodawanie(dzial)
