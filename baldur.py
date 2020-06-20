import win32api, win32con, win32gui
import time
import os
import keyboard
import pytesseract
import pyscreenshot as sc
import matplotlib.pyplot as plt

from pynput.mouse import Button, Controller

class Baldur:

    rollCounter = 0
    numbers = {}

    def __init__(self, bestRoll = 0):
        self.bestRoll = bestRoll

    def roll(self, wndPosize):
        win32api.SetCursorPos((wndPosize[0] + 440, wndPosize[1] + 695))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
        time.sleep(0.1)

        self.rollCounter += 1

        x = wndPosize[0] + 360
        y = wndPosize[1] + 615
        img = sc.grab(bbox=(x, y, x + 80, y + 20), backend="mss", childprocess=False)  # X1,Y1,X2,Y2

        img.save('box.png')

        custom_config = r'-c tessedit_char_whitelist=0123456789 --oem 0'

        roll = pytesseract.image_to_string(img, config=custom_config)

        if not roll in self.numbers:
            self.numbers[roll] = 1
        else:
            self.numbers[roll] += 1

        return int(roll)

    def save(self, wndPosize):
        time.sleep(1)
        win32api.SetCursorPos((wndPosize[0] + 140, wndPosize[1] + 695))
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
        time.sleep(0.5)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
        time.sleep(1)
        

class Wnd:
    def getWindowCallback(self, hwnd, extra):
        if "Baldur" in win32gui.GetWindowText(hwnd):
            rect = win32gui.GetWindowRect(hwnd)
            self.x = rect[0]
            self.y = rect[1]
            self.w = rect[2] - self.x
            self.h = rect[3] - self.y

    def __init__(self):
        self.refresh()

    def refresh(self):
        win32gui.EnumWindows(self.getWindowCallback, None)

    def getPosize(self):
        return (self.x, self.y, self.w, self.h)
wnd = Wnd()
bg = Baldur(90)

loop = True

def stop():

    numbers = sorted(bg.numbers.items(), key=lambda x: x[1])
    height = []
    left = []
    labels = []
    
    i = 0
    for num in numbers:
        height.append(num[1])
        labels.append(num[0])
        left.append(i)
        i += 1

    plt.bar(left, height, tick_label=labels, width=0.8, color = ['red'])

    plt.xlabel('Liczba')
    plt.ylabel('Ilosc wystąpien')
    plt.title('test')

    loop = False
    plt.show()

    print(numbers)


keyboard.add_hotkey('q', lambda: stop())
keyboard.wait('a')

while loop:
    currRoll = bg.roll(wnd.getPosize())

    print("Current roll: ", currRoll, ", best roll: ", bg.bestRoll)

    if currRoll > bg.bestRoll:
        bg.save(wnd.getPosize())
        bg.bestRoll = currRoll
        print("******************* NEW BEST ROLL! : ", bg.bestRoll, " **********************")
