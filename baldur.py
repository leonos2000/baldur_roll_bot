import win32api, time, os, keyboard, win32con, pytesseract, pyscreenshot as sc
from pynput.mouse import Button, Controller

keyboard.wait('a')

def roll():
    win32api.SetCursorPos((1200,1000))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_ABSOLUTE,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP|win32con.MOUSEEVENTF_ABSOLUTE,0,0)
    time.sleep(0.1)

def save():
    time.sleep(1)
    win32api.SetCursorPos((900,1000))
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_ABSOLUTE,0,0)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP|win32con.MOUSEEVENTF_ABSOLUTE,0,0)
    time.sleep(1)

def ocr():
    img = sc.grab(bbox=(1120, 920, 1200, 940), backend="mss", childprocess=False)  # X1,Y1,X2,Y2

    custom_config = r'-c tessedit_char_whitelist=0123456789 --oem 0'
    return pytesseract.image_to_string(img, config=custom_config)   


bestRoll = 9

keyboard.add_hotkey('q', lambda: os._exit(0))

while 1:
    roll()

    # time.sleep(0.05)

    currRoll = int(ocr())

    print("Current roll: ", currRoll, ", best roll: ", bestRoll)

    if currRoll > bestRoll:
        save()
        bestRoll = currRoll
        print("******************* NEW BEST ROLL! : ", bestRoll, " **********************")
