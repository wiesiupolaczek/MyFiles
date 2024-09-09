import sys, time
import sevseg

def timer(secondsLeft = 30,text="BOOM"):


    try:
        while True:
            print('\n' * 60)


            hours = str(secondsLeft // 3600)

            minutes = str((secondsLeft % 3600) // 60)

            seconds = str(secondsLeft % 60)

            # Get the digit strings from the sevseg module:
            hDigits = sevseg.getSevSegStr(hours, 2)
            hTopRow, hMiddleRow, hBottomRow = hDigits.splitlines()

            mDigits = sevseg.getSevSegStr(minutes, 2)
            mTopRow, mMiddleRow, mBottomRow = mDigits.splitlines()

            sDigits = sevseg.getSevSegStr(seconds, 2)
            sTopRow, sMiddleRow, sBottomRow = sDigits.splitlines()


            print(hTopRow    + '     ' + mTopRow    + '     ' + sTopRow)
            print(hMiddleRow + '  *  ' + mMiddleRow + '  *  ' + sMiddleRow)
            print(hBottomRow + '  *  ' + mBottomRow + '  *  ' + sBottomRow)

            if secondsLeft == 0:
                print()
                print('    * * * * {text}* * * *')
                break
            print()
            print('Press Ctrl-C to quit.')


            time.sleep(1)

            secondsLeft -= 1
    except KeyboardInterrupt:
        sys.exit()


timer()