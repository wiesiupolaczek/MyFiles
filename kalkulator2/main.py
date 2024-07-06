def dodawanie(dzial):
    dzial = dzial.split("+")
    if len(dzial) != 1:
        wynik=int(dzial[0])+int(dzial[1])
        print(f"{dzial[0]}+{dzial[1]}={wynik}")
def odejmowanie(dzial):
    dzial = dzial.split("-")
    if len(dzial) != 1:
        wynik=int(dzial[0])-int(dzial[1])
        print(f"{dzial[0]}-{dzial[1]}={wynik}")

def mnozenie(dzial):
    dzial = dzial.split("*")
    if len(dzial) != 1:
        wynik=int(dzial[0])*int(dzial[1])
        print(f"{dzial[0]}*{dzial[1]}={wynik}")

def dzielenie(dzial):
    dzial = dzial.split("/")
    if len(dzial) != 1:
        try:
            wynik=int(dzial[0])/int(dzial[1])
        except ZeroDivisionError:
            print("Nie mozna dzielic przez 0")
        print(f"{dzial[0]}/{dzial[1]}={wynik}")




if __name__ == '__main__':
    q=1
    print("Instrukcje:\nQ,q-wyjscie\n' + ' - dodawanie\n' - ' - odejmowanie\n' / ' - dzielenie\n' * ' - mnozenie")
    while q==1:
        dzial=input("Dzialanie:\n")
        if dzial == "q" or dzial == "Q":
            q=2
            break;
        else:

            dzielenie(dzial)
            mnozenie(dzial)
            odejmowanie(dzial)
            dodawanie(dzial)
