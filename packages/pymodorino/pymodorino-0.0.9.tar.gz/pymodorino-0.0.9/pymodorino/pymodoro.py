#!/usr/bin/env python

import argparse
import time
import threading
import sys
import os
import warnings
from blessed import Terminal
from notifypy import Notify
from pymodorino.utils import getRemainingTime, minutesToSeconds, printMessage

DEBUG = True
if not DEBUG:
    warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument('-w', type=float, default=25, help='Focus/work minutes. (default: 25m)')
parser.add_argument('-b', type=float, default=5, help='Break minutes. (default: 5m)')
parser.add_argument('-s', help='Wav file to use for the notifications. (default: ./oi.wav)')

args = parser.parse_args()

notification = Notify(
    default_notification_title="Pymodorino timer",
    default_notification_application_name="Pymodorino",
    default_notification_icon=  os.path.join(os.path.dirname(__file__), "pomodorino.png"),
    default_notification_audio= args.s or os.path.join(os.path.dirname(__file__), "oi.wav")
)

inputChar = ''          # Character to be used to eventually stop the program
t = Terminal()


def quitPomodoro():
    print('\n'*10)
    sys.exit()

def askForConfirmation(message):
    answer = ""
    while answer != "y" and answer != "n":
        printMessage(f"{message}(y/n): ", terminal=t)
        answer = t.inkey().lower()

    return answer == "y"

def sendNotification(message):
    notification.message = message
    notification.send()

class InputBuffer(threading.Thread):
    currChar = None
    __running = True

    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        # Gets input buffer char every second
        while self.__running:
            self.currChar = t.inkey(timeout=1)

    def stop(self):
        self.__running = False


class Timer():
    __isBreak = False
    inputBuffer = None

    def __init__(self, work_m, break_m):
        self.__WORK_m = work_m
        self.__BREAK_m = break_m
        self.__timeLeft = minutesToSeconds(args.w)

    def start(self):
        self.inputBuffer = InputBuffer()
        self.inputBuffer.daemon = True
        self.inputBuffer.start()

        msgPrefix = "BREAK" if self.__isBreak else "WORKING"

        def checkQuitChar():
            return self.inputBuffer.currChar == 'q'

        try:
            while self.__timeLeft >= 0 and not checkQuitChar():
                    printMessage(f"[{msgPrefix}]: Time remaining: {t.bold + getRemainingTime(self.__timeLeft)}", terminal=t)
                    self.__timeLeft -= 1
                    time.sleep(1)

            self.inputBuffer.stop()

            if checkQuitChar():
                quitPomodoro()
            else:
                if self.__isBreak:
                    sendNotification("Break time is up. Get to work!")
                    if askForConfirmation("Start working again?"):
                        self.__isBreak = False
                        self.__timeLeft = minutesToSeconds(self.__WORK_m) 
                        self.start()
                else:
                    sendNotification("Good work, you may take a break!")
                    if askForConfirmation("Time is up. Start break?"):
                        self.__isBreak = True
                        self.__timeLeft = minutesToSeconds(self.__BREAK_m) 
                        self.start()

        except (KeyboardInterrupt, Exception):
            quitPomodoro()


def main():
    with t.cbreak(), t.hidden_cursor():
        timer = Timer(args.w, args.b)
        timer.start()

if __name__ == "__main__":
    main()