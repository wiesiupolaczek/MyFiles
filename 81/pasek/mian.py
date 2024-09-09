import time,random

BAR = chr(9608)



def main():
    bytesDownloaded = 0
    downloadSize = 4096

    while bytesDownloaded < downloadSize:
        bytesDownloaded += random.randint(1,100)

        barStr = getProgressBar(bytesDownloaded,downloadSize)

        print(barStr,end="", flush=True)

        time.sleep(0.2)

        print("\b" * len(barStr),end="",flush=True)

def getProgressBar(progress, total, barWidth=40):
    progressBar = ""
    progressBar += "["

    if progress > total:
        progress = total
    if progress < 0:
        progress = 0
    numberOfBars = int((progress / total) * barWidth)

    progressBar += BAR * numberOfBars
    progressBar += " " * (barWidth - numberOfBars)
    progressBar += "]"

    percent = round(progress / total * 100, 1)
    progressBar += " " + str(percent) + "%"

    progressBar += " " + str(progress) + "/" + str(total)
    return progressBar



if __name__ == "__main__":
    main()

print(BAR)