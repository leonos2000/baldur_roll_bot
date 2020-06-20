import win32api, win32con, win32gui
import time
import os
import keyboard
import pytesseract
import pyscreenshot as sc
from pynput.mouse import Button, Controller

class Baldur:

    def __init__(self, bestRoll = 0):
        self.bestRoll = bestRoll

    def roll(self, wndPosize):
        win32api.SetCursorPos((wndPosize[0] + 440, wndPosize[1] + 695))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
        time.sleep(0.1)

        x = wndPosize[0] + 360
        y = wndPosize[1] + 615
        img = sc.grab(bbox=(x, y, x + 80, y + 20), backend="mss", childprocess=False)  # X1,Y1,X2,Y2

        img.save('box.png')

        custom_config = r'-c tessedit_char_whitelist=0123456789 --oem 0'
        return pytesseract.image_to_string(img, config=custom_config)   

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
        win32gui.EnumWindows(self.getWindowCallback, None)

    def refresh(self):
        win32gui.EnumWindows(self.getWindowCallback, None)

    def getPosize(self):
        return (self.x, self.y, self.w, self.h)


wnd = Wnd()
bg = Baldur()

keyboard.add_hotkey('q', lambda: os._exit(0))
keyboard.wait('a')

while 1:
    currRoll = int(bg.roll(wnd.getPosize()))

    print("Current roll: ", currRoll, ", best roll: ", bg.bestRoll)

    if currRoll > bg.bestRoll:
        bg.save(wnd.getPosize())
        bg.bestRoll = currRoll
        print("******************* NEW BEST ROLL! : ", bg.bestRoll, " **********************")
