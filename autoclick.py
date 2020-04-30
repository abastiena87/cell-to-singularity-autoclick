import threading

import pyautogui
import keyboard  # using module keyboard

print('Press Ctrl-C to quit.')
pyautogui.PAUSE = 0.001

count = 0
is_run = False


def auto_click():
    global count, is_run
    try:
        while True:
            if keyboard.is_pressed('q'):  # if key 'q' is pressed
                is_run = True
            if keyboard.is_pressed('w'):  # if key 'q' is pressed
                is_run = False

            if is_run:
                # x, y = pyautogui.position()
                # positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
                # print(positionStr)
                pyautogui.click(543, 261)
                # pyautogui.click(716, 315)
                # pyautogui.click(918, 456)
                # if count > 50:
                #     pyautogui.click(470, 160)
                # pyautogui.click(470, 210)
                # pyautogui.click(470, 259)
                # pyautogui.click(470, 307)
                # pyautogui.click(470, 352)
                # pyautogui.click(470, 402)
                # pyautogui.click(470, 442)
                # pyautogui.click(470, 500)

                # # first dino
                # # pyautogui.click(280, 191)
                # pyautogui.click(400, 204)
                #
                # # pyautogui.click(275, 266)
                # pyautogui.click(400, 275)
                #
                # pyautogui.click(400, 350)
                # pyautogui.click(400, 413)
                # pyautogui.click(400, 484)
                # pyautogui.click(400, 558)
                # pyautogui.click(400, 621)
                # pyautogui.click(400, 696)
                # pyautogui.click(400, 770)

                #     count = 0
                # else:
                #     count += 1
    except KeyboardInterrupt:
        print('\nDone.')


threads = list()
for index in range(3):
    x = threading.Thread(target=auto_click)
    threads.append(x)
    x.start()
