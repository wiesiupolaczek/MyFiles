import time,random

BAR = chr(9608)



def main():
    l=0
    while True:

        barStr = getProgressBar(l)

        print(barStr,end="", flush=True)

        time.sleep(0.5)

        print("\b" * len(barStr),end="",flush=True)
        l += 1
def getProgressBar(l):

    wiatrak = ["|","/","---","\\"]

    progressBar = wiatrak[l%4]

    return progressBar



if __name__ == "__main__":
    main()
