import win32api, win32con, win32gui
import time
import os
import keyboard
import pytesseract
import pyscreenshot as sc
import matplotlib.pyplot as plt
import math

from pynput.mouse import Button, Controller

class Baldur:
    rollCounter = 0
    numbers = {}
    rollin = True

    def __init__(self, bgVersion = 'BG2', bestRoll = 0):
        self.bestRoll = bestRoll
        if 'BG2' in bgVersion:
            self.rollButtonOffsetX = 440
            self.rollButtonOffsetY = 695

            self.scOffsetX = 360
            self.scOffsetY = 615

            self.saveButtonOffsetX = 140
            self.saveButtonOffsetY = 695

        elif 'SOD' in bgVersion:
            self.rollButtonScaleX = 31
            self.rollButtonScaleY = 67

            self.scScaleX1 = 38
            self.scScaleY1 = 58
            
            self.scScaleX2 = 40
            self.scScaleY2 = 61

            self.saveButtonScaleX = 30
            self.saveButtonScaleY = 72

    def scalePosX(self, wndPosize, scale):
        return round(wndPosize[0] + (wndPosize[2] * scale / 100))

    def scalePosY(self, wndPosize, scale):
        return round(wndPosize[1] + (wndPosize[3] * scale / 100))

    def roll(self, wndPosize):
        win32api.SetCursorPos((self.scalePosX(wndPosize, self.rollButtonScaleX), self.scalePosY(wndPosize, self.rollButtonScaleY)))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
        time.sleep(0.1)

        self.rollCounter += 1

        x1 = self.scalePosX(wndPosize, self.scScaleX1)
        y1 = self.scalePosY(wndPosize, self.scScaleY1)
        x2 = self.scalePosX(wndPosize, self.scScaleX2)
        y2 = self.scalePosY(wndPosize, self.scScaleY2)
        img = sc.grab(bbox=(x1, y1, x2, y2), backend="mss", childprocess=False)  # X1,Y1,X2,Y2

        custom_config = r'-c tessedit_char_whitelist=0123456789 --oem 0 --psm 7'

        roll = pytesseract.image_to_string(img, config=custom_config)

        if not roll in self.numbers:
            self.numbers[roll] = 1
        else:
            self.numbers[roll] += 1

        return int(roll)

    def save(self, wndPosize):
        time.sleep(1)
        win32api.SetCursorPos((self.scalePosX(wndPosize, self.saveButtonScaleX), self.scalePosY(wndPosize, self.saveButtonScaleY)))
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
        time.sleep(0.5)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
        time.sleep(1)
        

class Wnd:
    def getWindowCallback(self, hwnd, extra):
        if "Baldur" in win32gui.GetWindowText(hwnd):
            rect = win32gui.GetWindowRect(hwnd)
            if rect[0] > 0:
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
        a
wnd = Wnd()
bg = Baldur('SOD', 0)

def stop():
    bg.rollin = False

keyboard.add_hotkey('q', lambda: stop())
keyboard.wait('a')

while bg.rollin:
    currRoll = bg.roll(wnd.getPosize())

    print("Current roll: ", currRoll, ", best roll: ", bg.bestRoll)

    if currRoll > bg.bestRoll:
        bg.save(wnd.getPosize())
        bg.bestRoll = currRoll
        print("******************* NEW BEST ROLL! : ", bg.bestRoll, " **********************")

numbers = sorted(bg.numbers.items(), key=lambda x: int(x[0]))
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

plt.xlabel('Rolled number')
plt.ylabel('Occurrences')
plt.title('Made ' + str(bg.rollCounter) + ' rolls')

plt.show()