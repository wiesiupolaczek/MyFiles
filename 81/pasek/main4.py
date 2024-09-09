import time,random

BAR = chr(9608)



def main():
    lop = 1
    while True:

        for i in range(4):
            barStr = getProgressBar(i,lop)

            print(barStr,end="", flush=True)

            time.sleep(0.4)

            print("\b" * len(barStr),end="",flush=True)
        lop = lop * -1

def getProgressBar(i,lop):
    progressBar = ""
    progressBar += "["



    if lop == 1:
        progressBar += " " * i
        progressBar += "===="
        progressBar += " " * (4-i)
        progressBar += "]"

    if lop == -1:
        progressBar += " " * (4 - i)
        progressBar += "===="
        progressBar += " " * i
        progressBar += "]"
    return progressBar


if __name__ == "__main__":
    main()

