import os
import queue
import sys
import tkinter as tk

import pyautogui
import keyboard
import threading
import pickle

if not os.geteuid() == 0:
    sys.exit("\nOnly root can run this script\n")

lock = threading.Lock()

is_add_point = False
current_point = []

point_data = []
point_upgrade = []

point_data_enable = True
point_upgrade_enable = True

try:
    filehandler = open('data.pkl', 'rb')
    object = pickle.load(filehandler)
    point_data, point_upgrade = object
except Exception:
    print('Load data failed')

event_queue = queue.Queue()

print('Press Ctrl-C to quit.')
pyautogui.PAUSE = 0.001

count = 0
is_run = False


def start_event():
    print('start')
    global count, is_run

    while True:
        if keyboard.is_pressed('q') and not is_run:  # if key 'q' is pressed
            is_run = True
            for point in point_data:
                x, y, z = point
                if z:
                    threading.Thread(target=auto_click, daemon=True, args=(x, y)).start()
        if keyboard.is_pressed('w'):  # if key 'q' is pressed
            is_run = False


def auto_click(x, y):
    global count, is_run
    try:
        while True:
            if is_run:
                pyautogui.click(x, y)
                lock.acquire()
                try:
                    if count > 50:
                        for x1, y1, z1 in point_upgrade:
                            if z1:
                                pyautogui.click(x1, y1)

                        count = 0
                    else:
                        count += 1
                finally:
                    lock.release()

            else:
                break

    except KeyboardInterrupt:
        print('\nDone.')


def delete_all(upgrade):
    global point_upgrade
    global point_data
    if upgrade:
        point_upgrade = []
    else:
        point_data = []
    update()


def toggle_all(upgrade):
    global point_upgrade
    global point_data
    global point_data_enable
    global point_upgrade_enable
    if upgrade:
        for point in point_upgrade:
            point[2] = point_upgrade_enable
        point_upgrade_enable = not point_upgrade_enable
    else:
        for point in point_data:
            point[2] = point_data_enable
        point_data_enable = not point_data_enable
    update()


def handle_delete(ind, upgrade):
    if upgrade == 0:
        del point_data[ind]
    else:
        del point_upgrade[ind]
    update()


def handle_enable(ind, upgrade):
    if upgrade == 0:
        point_data[ind][2] = not point_data[ind][2]
    else:
        point_upgrade[ind][2] = not point_upgrade[ind][2]
    update()


def update():
    # display
    global is_run
    global frm_click_point
    global frm_point_upgrade
    is_run = False
    frm_click_point.destroy()
    frm_point_upgrade.destroy()
    frm_click_point = tk.Frame(master=frm_point, padx=10)
    frm_point_upgrade = tk.Frame(master=frm_point, padx=10)
    frm_click_point.grid(row=1, column=0, sticky="w")
    frm_point_upgrade.grid(row=1, column=1, sticky="w")
    if len(point_data) > 0:
        for ind in range(len(point_data)):
            i = f'{ind + 1},'
            x = f'x: {point_data[ind][0]}'
            y = f'y: {point_data[ind][1]}'
            z = 'Enable' if not point_data[ind][2] else 'Disable'
            tk.Label(master=frm_click_point, text=i).grid(row=ind, column=0, sticky="w")
            tk.Label(master=frm_click_point, text=x).grid(row=ind, column=1, sticky="w")
            tk.Label(master=frm_click_point, text=y).grid(row=ind, column=2, sticky="w")

            btn_enable = tk.Button(
                master=frm_click_point,
                text=z,
                command=lambda a=ind, b=0: handle_enable(a, b)
            )

            btn_enable.grid(row=ind, column=3, sticky="w")

            tk.Button(
                master=frm_click_point,
                text="Del",
                command=lambda a=ind, b=0: handle_delete(a, b)
            ).grid(row=ind, column=4, sticky="w")

    if len(point_upgrade) > 0:
        for ind in range(len(point_upgrade)):
            i = f'{ind + 1},'
            x = f'x: {point_upgrade[ind][0]}'
            y = f'y: {point_upgrade[ind][1]}'
            z = 'Enable' if not point_upgrade[ind][2] else 'Disable'
            tk.Label(master=frm_point_upgrade, text=i).grid(row=ind, column=0, sticky="w")
            tk.Label(master=frm_point_upgrade, text=x).grid(row=ind, column=1, sticky="w")
            tk.Label(master=frm_point_upgrade, text=y).grid(row=ind, column=2, sticky="w")
            tk.Button(
                master=frm_point_upgrade,
                text=z,
                command=lambda a=ind, b=1: handle_enable(a, b)
            ).grid(row=ind, column=3, sticky="w")

            tk.Button(
                master=frm_point_upgrade,
                text="Del",
                command=lambda a=ind, b=1: handle_delete(a, b)
            ).grid(row=ind, column=4, sticky="w")

    object_pi = [point_data, point_upgrade]
    file_pi = open('data.pkl', 'wb')
    pickle.dump(object_pi, file_pi)


def handle_add_point():
    if len(current_point) > 0:
        if not is_upgrade.get():
            point_data.append(current_point)
        else:
            point_upgrade.append(current_point)
        update()


def listen_point():
    global is_add_point
    global current_point
    try:
        while True:
            if keyboard.is_pressed('r') and is_add_point:
                x, y = pyautogui.position()
                lbl_position["text"] = f"{x},{y}"
                is_add_point = False
                current_point = [x, y, True]

    except KeyboardInterrupt:
        print('\nDone.')


def handle_choose_point():
    global is_add_point
    if not is_add_point:
        is_add_point = True


# Set-up the window
window = tk.Tk()
window.title("Cells auto click")
window.resizable(width=False, height=False)

# Choose Point
frm_choose = tk.Frame(master=window)

lbl_position = tk.Label(master=frm_choose)
lbl_point = tk.Label(master=frm_choose, text="Point")
lbl_is_upgrade = tk.Label(master=frm_choose, text="Is Upgrade")
is_upgrade = tk.BooleanVar()
cb_is_upgrade = tk.Checkbutton(master=frm_choose, variable=is_upgrade, onvalue=True, offvalue=False)
btn_choose = tk.Button(
    master=frm_choose,
    text="Choose Point",
    command=handle_choose_point
)

btn_add = tk.Button(
    master=frm_choose,
    text="Add Point",
    command=handle_add_point
)

lbl_point.grid(row=0, column=0, sticky="w")
lbl_position.grid(row=0, column=1, sticky="e")
lbl_is_upgrade.grid(row=1, column=0, sticky="e")
cb_is_upgrade.grid(row=1, column=1, sticky="e")
btn_choose.grid(row=0, column=2, sticky="e")
btn_add.grid(row=2, column=1, sticky="e")

frm_choose.grid(row=0, column=0)

# List Point
frm_point = tk.Frame(master=window)

lbl_point = tk.Label(master=frm_point, text='Click Point').grid(row=0, column=0)
lbl_upgrade = tk.Label(master=frm_point, text='Upgrade Point').grid(row=0, column=1)

frm_click_point = tk.Frame(master=frm_point)
frm_point_upgrade = tk.Frame(master=frm_point)
update()

tk.Button(
    master=frm_point,
    text="Del All",
    command=lambda a=True: delete_all(False)
).grid(row=2, column=0)

tk.Button(
    master=frm_point,
    text="Del All",
    command=lambda a=True: delete_all(True)
).grid(row=2, column=1)

tk.Button(
    master=frm_point,
    text="Toggle",
    command=lambda a=True: toggle_all(False)
).grid(row=3, column=0)

tk.Button(
    master=frm_point,
    text="Toggle",
    command=lambda a=True: toggle_all(True)
).grid(row=3, column=1)

frm_point.grid(row=1, column=0)

# background task
threading.Thread(target=listen_point, daemon=True).start()
threading.Thread(target=start_event, daemon=True).start()

# Run the application
window.mainloop()
